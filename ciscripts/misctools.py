"""Miscellaneous tools for OpenReproLab 2026-2027 CI scripts.

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

import os


def path_of_repo(path=None):
    """Return path of Git repository containing given path.

    Parameters
    ----------
    path: str
        A path that is supposed to be located somewhere in a Git repository. If
        None, then this function returns the path of the Git repository
        containing this module.

    Returns
    -------
    str
        The path of the Git repository that contains given path.

    Notes
    -----
    Given path does not have to exist to find the corresponding Git repository.
    For example, if /home/myself/myrepo is an existing Git repository, then
    path_of_repo("/home/myself/myrepo/myfile.txt") will return
    "/home/myself/myrepo" even if myfile.txt does not exists.

    """
    abspath = os.path.abspath(__file__ if path is None else path)
    if os.path.isdir(os.path.join(abspath, ".git")):
        return abspath
    parent = os.path.dirname(abspath)
    if parent == abspath:
        msg = "Could not determine path to git repository."
        raise RuntimeError(msg)
    else:
        return path_of_repo(parent)
