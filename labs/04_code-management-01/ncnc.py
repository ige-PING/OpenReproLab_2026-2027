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
    stdscr.getkey()


class Application:
    """Cladd to handle the ncnc application."""

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
        If filepath is None, only a bare-bone initialization is done.

        """
        curses.curs_set(0)
        self.stdscr = stdscr
        if filepath is None:
            return

        self.ds = xr.open_dataset(filepath)

        # Hard-coded dimensions of the areas of the application
        self.dimlist_width = 40
        self.dimlist_height = 20
        self.vattrs_height = 10

        # Calculated dimensions of the areas of the application
        self.varlist_width = curses.COLS - 1 - self.dimlist_width
        self.varlist_height = curses.LINES - 2 - self.vattrs_height
        self.vattrs_width = self.varlist_width
        self.stats_height = curses.LINES - 2 - self.dimlist_height
        self.stats_width = self.dimlist_width

        # For convenience, the location of the top-left corner of each area
        self.xy1_varlist = (1, 0)
        self.xy1_dimlist = (1, self.varlist_width + 1)
        self.xy1_vattrs = (self.varlist_height + 2, 0)
        self.xy1_stats = (self.dimlist_height + 2, self.varlist_width + 1)

        # For convenience, the location of the bottom-right corner of each area
        self.xy2_varlist = (self.varlist_height, self.varlist_width - 1)
        self.xy2_dimlist = (self.dimlist_height, curses.COLS - 1)
        self.xy2_vattrs = (curses.LINES - 1, self.vattrs_width - 1)
        self.xy2_stats = (curses.LINES - 1, curses.COLS - 1)

        # Draw the outline of the window
        self.draw_header()
        self.draw_borders()
        self.refresh()

        # Create and show the pad for the list of variables
        lines = self.get_variables()
        self.varlist = curses.newpad(
            len(lines),
            max(len(line) for line in lines),
        )
        for i, line in enumerate(lines):
            self.varlist.addstr(i, 0, line)
        self.varlist.refresh(0, 0, *self.xy1_varlist, *self.xy2_varlist)

        # Create and show the pad for the list of dimensions
        lines = self.get_dimensions()
        self.dimlist = curses.newpad(
            len(lines),
            max(len(line) for line in lines),
        )
        for i, line in enumerate(lines):
            self.dimlist.addstr(i, 0, line)
        self.dimlist.refresh(0, 0, *self.xy1_dimlist, *self.xy2_dimlist)

    def draw_header(self):
        """Draw the application's header."""
        self.addstr(0, 0, hcenter("ncnc"), curses.A_REVERSE)

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

    def error(self, msg):
        """Show error message.

        Parameters
        ----------
        msg: str
            The error message.

        Notes
        -----
        This method returns when the user presses a key.

        """
        self.clear()
        self.draw_header()
        y = (curses.LINES - 1) // 2
        self.addstr(y, 0, hcenter(msg))
        self.addstr(y + 1, 0, hcenter("Press any key to exit"))
        self.refresh()
        self.getkey()

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
        n = len(self.ds.variables)
        names = [None] * n
        dtypes = [None] * n
        dimensions = [None] * n
        for i, name in enumerate(self.ds.variables):
            names[i] = name
            dtypes[i] = self.ds.variables[name].dtype
            dimensions[i] = list(self.ds.variables[name].dims)
        names = right_pad_strings(names)
        dtypes = right_pad_strings(dtypes)
        for i in range(n):
            if len(dimensions[i]) > 0:
                dimensions[i] = "(" + ", ".join(dimensions[i]) + ")"
            else:
                dimensions[i] = ""
        return [f"{names[i]}  {dtypes[i]}  {dimensions[i]}" for i in range(n)]


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
