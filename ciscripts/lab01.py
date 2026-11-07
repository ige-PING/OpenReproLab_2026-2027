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
import sys

from misctools import Check, part_banner, path_of_repo

lab_dir = os.path.join(path_of_repo(), "labs", "01_ABC-of-repro-numerical-science")

part_checks = []

hello_world_file = "hello-world.txt"
part_checks.append(
    Check(
        'Push "Hello world" file to Github/Gitlab from command-line',
        os.path.exists(os.path.join(lab_dir, hello_world_file)),
        f'Check that you have added/commited/pushed the "{hello_world_file}" within the lab01 directory!',
    )
)

download_data_file = "download-data.py"
part_checks.append(
    Check(
        "Create Python script that downloads CSV data",
        os.path.exists(os.path.join(lab_dir, download_data_file)),
        f'Check that you have added/commited/pushed the "{download_data_file}" within the lab01 directory!',
    )
)

# Checklist summary

for index, check in enumerate(part_checks):
    part_banner(index + 1, check.part)
    print(check.not_ok_tips)
    print()

all_good = any([not result for result in part_checks])

if all_good:
    print("==> Lab completed succesfully, congratulations!")
    sys.exit(0)
else:
    print("==> Some checks failed, keep at it!")
    sys.exit(1)
