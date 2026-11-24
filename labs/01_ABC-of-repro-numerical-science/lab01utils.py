"""Script that downloads microplastic data used in Hough et al. (2026).

Copyright (C) Institut des Géosciences de l'Environnement, Grenoble.

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, version 3.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.

The DOI associated to the data that this script will download is:

    10.5281/zenodo.23046811

In order for the download process to be reproducible, it is important to
specify which Git commit contains the data : a0ba5c3a6a5e0271ef9860ea8a5f8b73fce0e44d

"""

import os
import subprocess

def download_file_from_github(base_url, repository, commit, filepath):

    """
    Download specific file from Github repository.

    Parameters
    ----------
    repository: str
        Name of the repository.
    commit: "a0ba5c3a6a5e0271ef9860ea8a5f8b73fce0e44d"
        Commit of interest (full hash).
    filepath
        File of interest within repository.

    """
        # Remove target file if already present
    try:
        os.remove(os.path.basename(filepath))
    except:
        pass

        # Download the file using wget
    url = "/".join([base_url, repository, commit, filepath])
    out = subprocess.run(["wget", url], capture_output=True, text=True)
    if out.returncode:
        msg = out.stderr
        raise RuntimeError(msg)