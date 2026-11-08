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

Zenodo seems to limit the number of wget requests that can be executed in a
given amount of time. We will therefore download the data from the
corresponding GitHub repository instead.

In order for the download process to be reproducible, it is important to
specify which Git commit contains the data we want. This is your task here.
Start from Zenodo (https://doi.org/10.5281/zenodo.23046811), and try to figure
out what is the specific GitHub commit that this Zenodo record refers to.

Downloading directly from Zenodo would be more reproducible (Zenodo is likely
to be around longer than Github) but more complex (we would need to use a
Zenodo-specific API). Since this is a learning exercise, we settled for
simplicity.

"""

import os
import subprocess

base_url = "https://raw.githubusercontent.com"
repository = "GEOS-Chem-IGE/hough2026_atmo-plast-emis_harmonize"
commit = "????"
filepath = "data/processed/obs_evangelou2026-revised.csv"

if __name__ == "__main__":
    # Download the file using wget
    url = "/".join([base_url, repository, commit, filepath])
    out = subprocess.run(["wget", url], capture_output=True, text=True)
    if out.returncode:
        msg = out.stdout[:-1].split("\n")
        raise RuntimeError(msg)
