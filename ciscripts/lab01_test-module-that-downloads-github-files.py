"""Script to check the module created in lab 01 of OpenReproLab 2026-2027.

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

import hashlib
import os
import sys

from orlcitools import path_of_repo

# Import the student's module
dir_lab = os.path.join(
    path_of_repo(),
    "labs",
    "01_ABC-of-repro-numerical-science",
)
sys.path = [dir_lab] + sys.path
from lab01utils import download_file_from_github

# Define the test cases
# (in order: repository, commit hash, file path, file sha256 hash)
to_test = [
    (
        "GEOS-Chem-IGE/hough2026_atmo-plast-emis_harmonize",
        "e05e7409e539d3967d81dfb810d36139ce829f5e",
        "utils/data.py",
        "abc839e083030d33e69b0378c00ef2a215d3943ab8ed0d7b27eb047ced9011d2",
    ),
    (
        "GEOS-Chem-IGE/hough2026_atmo-plast-emis_harmonize",
        "0cf560ec5c64bfd37ba795f7fbed1f7bb5f909c1",
        "utils/data.py",
        "98b0aea998ae2fbc5930026be9618a5a065f2415e58f190eba0e2eeecc0ad3d0",
    ),
    (
        "ige-PING/OpenReproLab_2026-2027",
        "3316cabd193e306b1b555ab05bf1632d8a38d5fe",
        "labs/01_ABC-of-repro-numerical-science/README.md",
        "ac5e9fbef40b9b875ceeb1a8637a655c76265d51bcd965ecf2d618b10ed13377",
    ),
]

# Run the tests
for repo, commit, filepath, expected_hash in to_test:
    basename = os.path.basename(filepath)

    if os.path.lexists(basename):
        msg = f'File "{basename}" already exists.'
        raise RuntimeError(msg)

    download_file_from_github(repo, commit, filepath)

    with open(os.path.basename(filepath), mode="rb") as f:
        digest = hashlib.file_digest(f, "sha256").hexdigest()

    os.remove(basename)

    if digest != expected_hash:
        msg = (
            'The function "download_file_from_github" did not '
            "pass all the tests."
        )
        raise ValueError(msg)
