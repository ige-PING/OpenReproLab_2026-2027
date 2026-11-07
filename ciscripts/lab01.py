"""Script to check answers of lab 02 of OpenReproLab 2026-2027.

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

from misctools import Verifier, path_of_repo, verify_lab

lab_dir = os.path.join(path_of_repo(), "labs", "01_ABC-of-repro-numerical-science")

parts = []

hello_world_file = "hello-world.txt"
parts.append(
    Verifier(
        'Push "Hello world" file to Github/Gitlab from command-line',
        lambda: os.path.exists(os.path.join(lab_dir, hello_world_file)),
        f'Check that you have added/commited/pushed the "{hello_world_file}" within the lab01 directory!',
    )
)

download_data_file = "download-data.py"


def check_download_script() -> bool:
    return os.path.exists(os.path.join(lab_dir, download_data_file))


parts.append(
    Verifier(
        "Create Python script that downloads CSV data",
        check_download_script,
        f'Check that you have added/commited/pushed the "{download_data_file}" within the lab01 directory!',
    )
)

verify_lab(parts)
