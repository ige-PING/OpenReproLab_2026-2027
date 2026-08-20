"""A ncurses program to explore NetCDF files.

Copyright (C) Institut des Géosciences de l'Environnement, Grenoble.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.

"""

import curses
import curses.panel

import xarray as xr


# ----------------#
# Main components #
# ----------------#


def ncexplorer(stdscr, filepath):
    """Main function for the ncurses application.

    Parameters
    ----------
    stdstr: curses.window
        The main curses window of the application.

    """
    stdscr.clear()
    app = Application(stdscr, filepath)
    while True:
        key = stdscr.getkey()
        if key == "q":
            return
        else:
            app.on_key_pressed(key)


class Application:
    """Class to handle the ncnc application."""

    def __init__(self, stdscr, filepath=None):
        """Initialize self.

        Parameters
        ----------
        stdstr: curses.window
            The main curses window of the application.
        filepath: str | None
            If not None, the path to the NetCDF file.

        Notes
        -----
        1. If filepath is None, only a bare-bone initialization is done.

        2. The window of the application is divided into four areas (plus a
           header, which is not shown on the graph below):

        |--------------------------------------------------------------------|
        |                                       |                            |
        | varlist                               | dimlist                    |
        | (a list of the variables)             | (a list of the dimensions) |
        |                                       |                            |
        |                                       |                            |
        |                                       |                            |
        |                                       |----------------------------|
        |                                       |                            |
        |                                       | stats                      |
        |---------------------------------------| (statistics on the         |
        |                                       | selected variable)         |
        | vattrs                                |                            |
        | (the attributes of selected variable) |                            |
        |                                       |                            |
        |                                       |                            |
        |--------------------------------------------------------------------|

        """
        curses.curs_set(0)
        self.stdscr = stdscr
        self.main = curses.panel.new_panel(self.stdscr)
        self.main.top()
        if filepath is None:
            return
        self.ds = xr.open_dataset(filepath)

        # Hard-coded dimensions of the areas of the application
        self.dimlist_width = 40

        # Dimensions of the areas that are computed dynamically
        self.vattrs_height = max(
            len(var.attrs) for _, var in self.ds.variables.items()
        )
        self.dimlist_height = len(self.ds.sizes)
        self.varlist_width = curses.COLS - 1 - self.dimlist_width
        self.varlist_height = curses.LINES - 2 - self.vattrs_height
        self.vattrs_width = self.varlist_width
        self.stats_height = curses.LINES - 2 - self.dimlist_height
        self.stats_width = self.dimlist_width

        # For convenience, the location of the top-left corner of each area
        self.yx1_varlist = (1, 0)
        self.yx1_dimlist = (1, self.varlist_width + 1)
        self.yx1_vattrs = (self.varlist_height + 2, 0)
        self.yx1_stats = (self.dimlist_height + 2, self.varlist_width + 1)

        # For convenience, the location of the bottom-right corner of each area
        self.yx2_varlist = (self.varlist_height, self.varlist_width - 1)
        self.yx2_dimlist = (self.dimlist_height, curses.COLS - 1)
        self.yx2_vattrs = (curses.LINES - 1, self.vattrs_width - 1)
        self.yx2_stats = (curses.LINES - 1, curses.COLS - 1)

        # Information about where we currently are in the list of variables
        self.varlist_top = 0
        self.varlist_current = 0

        # Draw the outline of the window
        self.draw_header()
        self.draw_borders()
        self.refresh()

        # Create and show the pad for the list of variables
        lines = self.get_variables()
        self.varlist = curses.newpad(
            len(lines),
            max(max(len(line) for line in lines), self.varlist_width),
        )
        for i, line in enumerate(lines):
            self.varlist.addstr(i, 0, line)
        self.varlist.chgat(self.varlist_current, 0, curses.A_REVERSE)
        self.draw_varlist()

        # Create and show the pad for the list of dimensions
        lines = self.get_dimensions()
        self.dimlist = curses.newpad(
            len(lines),
            max(max(len(line) for line in lines), self.dimlist_width),
        )
        for i, line in enumerate(lines):
            self.dimlist.addstr(i, 0, line)
        self.draw_dimlist()

        # Create and show the pad for the variables' attributes
        lines = self.get_vattrs()
        self.vattrs = curses.newpad(
            len(lines),
            max(max(len(line) for line in lines), self.vattrs_width),
        )
        for i, line in enumerate(lines):
            self.vattrs.addstr(i, 0, line)
        self.vattrs.refresh(0, 0, *self.yx1_vattrs, *self.yx2_vattrs)

        # Create but do not show the pad for the stastitics
        self.stats = curses.newpad(self.stats_height, self.stats_width)

        # Create but do not show the pad for the global attributes
        lines = self.get_gattrs()
        self.gattrs_nlines = len(lines)
        while len(lines) < curses.LINES - 1:
            lines.append("")
        self.gattrs = curses.panel.new_panel(
            curses.newpad(
                len(lines),
                max(max(len(line) for line in lines), curses.COLS - 1),
            )
        )
        for i, line in enumerate(lines):
            self.gattrs.window().addstr(i, 0, line)

    def __getattr__(self, name):
        """Convenience getattr function that falls back on self.stdscr.

        This gives transparent access to self.stdscr methods, provided they
        are NOT defined explicitly by the Application class definition.

        Parameters
        ----------
        name: str
            Name of the attribute to access (looked up in Application's native
            attributes first, and then, if not found yet, in self.stdscr).

        """
        return getattr(self.stdscr, name)

    @property
    def filepath(self):
        """The path to the NetCDF file."""
        return self.ds.encoding["source"]

    @property
    def ndims(self):
        """The number of dimensions in the file."""
        return len(self.ds.sizes)

    @property
    def nvars(self):
        """The number of variables in the file."""
        return len(self.ds.variables)

    @property
    def ngattrs(self):
        """The number of global attributes in the file."""
        return len(self.ds.attrs)

    def draw_header(self, text=None):
        """Draw the application's header.

        Parameters
        ----------
        text: str | None
            The text to show in the header (automatically created if None).

        """
        if text is None:
            text = f">> ncnc: exploring {self.filepath} <<"
        self.addstr(0, 0, hcenter(text), curses.A_BOLD)

    def draw_borders(self):
        """Draw the borders between the different areas of the application."""
        # Horizontal line between list of variables and variable attributes
        self.addstr(self.varlist_height + 1, 0, "-" * self.varlist_width)
        # Horizontal line between list of dimensions and statistics
        self.addstr(
            self.dimlist_height + 1,
            self.varlist_width + 1,
            "-" * self.dimlist_width,
        )
        # Vertical line between left and right areas
        for y in range(1, curses.LINES):
            self.addch(y, self.varlist_width, "|")

    def get_dimensions(self):
        """Returns a description of the dims of the underlying NetCDF file.

        Returns
        -------
        [str]
            A description of the dimensions of the underlying NetCDF file, as a
            list of character strings, each element describing one dimension.

        """
        return [f"{name} = {size}" for name, size in self.ds.sizes.items()]

    def get_variables(self):
        """Return a description of the variables of the underlying NetCDF file.

        Returns
        -------
        [str]
            A description of the variables of the underlying NetCDF file, as a
            list of character strings, each element describing one variable.

        """
        names = [None] * self.nvars
        dtypes = [None] * self.nvars
        dimensions = [None] * self.nvars
        for i, name in enumerate(self.ds.variables):
            names[i] = name
            dtypes[i] = str(self.ds.variables[name].dtype)
            dimensions[i] = list(self.ds.variables[name].dims)
        names = right_pad_strings(names)
        dtypes = right_pad_strings(dtypes)
        for i in range(self.nvars):
            if len(dimensions[i]) > 0:
                dimensions[i] = "(" + ", ".join(dimensions[i]) + ")"
            else:
                dimensions[i] = ""
        return [
            f"{names[i]}  {dtypes[i]}  {dimensions[i]}"
            for i in range(self.nvars)
        ]

    def get_vattrs(self):
        """Return a description of the var attrs of the underlying NetCDF file.

        Returns
        -------
        [str]
            A description of the variables' attributes of the underlying NetCDF
            file, as a list of character strings. This list contains blank
            lines so that we never show attributes of two variables at the same
            time.

        """
        attrs = []
        for vname, var in self.ds.variables.items():
            names = list(var.attrs.keys())
            values = [var.attrs[name] for name in names]
            names = right_pad_strings(names)
            for name, value in zip(names, values):
                attrs.append(f"{name}  {value}")
            attrs += [""] * (self.vattrs_height - len(names))
        return attrs

    def get_gattrs(self):
        """Return a description of the underlying NetCDF file's global attrs.

        Returns
        -------
        [str]
            A description of the global attributes of the underlying NetCDF
            file, as a list of character strings.

        """
        names = []
        values = []
        for name, value in self.ds.attrs.items():
            for i, line in enumerate(value.split("\n")):
                names.append(name if i == 0 else "")
                values.append(line)
        names = right_pad_strings(names)
        return [f"{name}  {value}" for name, value in zip(names, values)]

    def draw_varlist(self):
        """Draw the list of variables."""
        self.varlist.refresh(
            self.varlist_top,
            0,
            *self.yx1_varlist,
            *self.yx2_varlist,
        )

    def draw_dimlist(self):
        """Draw the list of dimensions."""
        self.dimlist.refresh(0, 0, *self.yx1_dimlist, *self.yx2_dimlist)

    def draw_vattrs(self):
        """Draw the currently selected variable's attributes."""
        self.vattrs.refresh(
            self.varlist_current * self.vattrs_height,
            0,
            *self.yx1_vattrs,
            *self.yx2_vattrs,
        )

    def draw_stats(self):
        """Draw the stats for the current variable."""
        # Clear what is already there
        line = " " * self.stats_width
        for i in range(self.stats_height - 1):
            self.stats.addstr(i, 0, line)
        self.stats.refresh(
            0,
            0,
            *self.yx1_stats,
            *self.yx2_stats,
        )

    @property
    def last_var_is_visible(self):
        """True iff the last variable of the list is visible."""
        return self.nvars - self.varlist_top < self.varlist_height

    @property
    def last_visible_var_is_selected(self):
        """True iff the last visible variable is selected."""
        return (
            self.varlist_current - self.varlist_top + 1 == self.varlist_height
        )

    def on_key_pressed(self, key):
        """Call back when a key is pressed.

        Parameters
        ----------
        key: str
            The key that was pressed.

        """
        key = str(key)
        if key in ("n", "KEY_DOWN"):
            self.move_down()
        elif key in ("p", "KEY_UP"):
            self.move_up()
        elif key == "G":
            self.move_all_the_way_down()
        elif key == "g":
            self.move_all_the_way_up()
        elif key == "a":
            self.navigate_gattrs()

    def move_down(self):
        """Call back for moving down the list of variables."""
        if self.varlist_current >= self.nvars - 1:
            return
        self.varlist.chgat(self.varlist_current, 0, curses.A_NORMAL)
        if self.last_visible_var_is_selected and not self.last_var_is_visible:
            self.varlist_top += 1
        self.varlist_current += 1
        self.varlist.chgat(self.varlist_current, 0, curses.A_REVERSE)
        self.draw_varlist()
        self.draw_vattrs()
        self.refresh()

    def move_up(self):
        """Call back for moving up the list of variables."""
        if self.varlist_current <= 0:
            return
        self.varlist.chgat(self.varlist_current, 0, curses.A_NORMAL)
        if self.varlist_current <= self.varlist_top:
            self.varlist_top -= 1
        self.varlist_current -= 1
        self.varlist.chgat(self.varlist_current, 0, curses.A_REVERSE)
        self.draw_varlist()
        self.draw_vattrs()
        self.refresh()

    def move_all_the_way_down(self):
        """Call back for moving all the way down the list of variables."""
        if self.last_var_is_visible and self.last_visible_var_is_selected:
            return
        self.varlist.chgat(self.varlist_current, 0, curses.A_NORMAL)
        self.varlist_top = self.nvars - self.varlist_height
        self.varlist_current = self.nvars - 1
        self.varlist.chgat(self.varlist_current, 0, curses.A_REVERSE)
        self.draw_varlist()
        self.draw_vattrs()
        self.refresh()

    def move_all_the_way_up(self):
        """Call back for moving all the way up the list of variables."""
        if self.varlist_current <= 0:
            return
        self.varlist.chgat(self.varlist_current, 0, curses.A_NORMAL)
        self.varlist_top = 0
        self.varlist_current = 0
        self.varlist.chgat(self.varlist_current, 0, curses.A_REVERSE)
        self.draw_varlist()
        self.draw_vattrs()
        self.refresh()

    def navigate_gattrs(self):
        """Show and navigate the global attributes."""
        self.gattrs.top()
        title = f">> ncnc: global attributes of {self.filepath} <<"
        self.draw_header(text=title)
        pad = self.gattrs.window()
        top = 0
        pad.refresh(top, 0, 1, 0, curses.LINES - 1, curses.COLS - 1)
        while True:
            key = str(self.getkey())
            if key == "q":
                break
            refresh = True
            if key in ("n", "KEY_DOWN"):
                top = min(top + 1, self.gattrs_nlines - 1)
            elif key in ("p", "KEY_UP"):
                top = max(top - 1, 0)
            else:
                refresh = False
            if refresh:
                pad.refresh(top, 0, 1, 0, curses.LINES - 1, curses.COLS - 1)
        self.draw_header()
        self.draw_borders()
        self.draw_varlist()
        self.draw_vattrs()
        self.draw_dimlist()
        self.draw_stats()
        self.refresh()


# -------------------------------------#
# Utility functions: character strings #
# -------------------------------------#


def hcenter(text):
    """Center given text horizontally.

    Parameters
    ----------
    text: str
        The text to center horizontally (should not contain newlines).

    """
    n = (curses.COLS - len(text)) // 2
    text = " " * n + text
    return text + " " * (curses.COLS - len(text))


def right_pad_strings(strings):
    """Pad all strings in given list so that they all have the same length.

    Parameters
    ----------
    strings: [str]
        List of character strings to pad.

    Returns
    -------
    [str]
        A copy of the given list of strings where all strings have been
        right-padded to have equal length.

    """
    if len(strings) == 0:
        return []
    n_chars = max(len(string) for string in strings)
    format_ = f"%-{n_chars}s"
    return [format_ % string for string in strings]


# -------------#
# Main program #
# -------------#


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="ncnc",
        description="Explore the contents of a NetCDF file.",
        epilog="This programme is released under the GPL-3.0-only license.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "file",
        help="Path to NetCDF file.",
    )
    args = parser.parse_args()

    curses.wrapper(ncexplorer, args.file)
