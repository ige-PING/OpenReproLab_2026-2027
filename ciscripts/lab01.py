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
import re
import subprocess

from orlcitools import VerifiedResult, Verifier, path_of_repo, verify_lab

dir_lab = os.path.join(
    path_of_repo(),
    "labs",
    "01_ABC-of-repro-numerical-science",
)
could_not_open_file = (
    "Could not open file %s. It might not exist or it "
    "might be in an unexpected location."
)
verifiers = []


# ----------- #
# Hello World #
# ----------- #


def verify_hello_world():
    """Verifier function for the Hello World part."""
    filename = "hello-world.txt"
    filepath = os.path.join(dir_lab, filename)
    try:
        f = open(filepath)
    except:
        return VerifiedResult(False, could_not_open_file % filename)
    content = f.read()
    try:
        f.close()
    except:
        pass
    for c in " \t\n!-_":
        content = content.replace(c, "")
    if content.lower() != "welcometoopenreprolab":
        return VerifiedResult(
            False,
            f'File "{filename}" was found but its content is incorrect.',
        )
    return VerifiedResult(True, None)


verifiers.append(
    Verifier(
        'Push "Hello World" file to Github/Gitlab from command-line',
        verify_hello_world,
    )
)


# --------------------------- #
# Download microplastics data #
# --------------------------- #


def verify_download_data():
    """Verifier function for the data-downloading part."""

    # Verify that the data file has not been commited
    dataname = "obs_evangelou2026-revised.csv"
    datapath = os.path.join(dir_lab, dataname)
    if os.path.lexists(datapath):
        return VerifiedResult(
            False,
            f'Data file "{dataname}" should not be commited.',
        )

    # Verify that the .gitignore is correct
    ignorename = ".gitignore"
    ignorepath = os.path.join(dir_lab, ignorename)
    try:
        f = open(ignorepath)
    except:
        return VerifiedResult(False, could_not_open_file % ignorename)
    lines = [line.strip() for line in f.readlines()]
    try:
        f.close()
    except:
        pass
    accepted = (dataname, f"./{dataname}", "*.csv", "**/*.csv")
    if all(line not in accepted for line in lines):
        return VerifiedResult(
            False,
            f"Missing rule to ignore {dataname} in gitignore.",
        )

    # Check that the commit in the script is the correct one
    scriptname = "download-micro-plastics-data.py"
    scriptpath = os.path.join(dir_lab, scriptname)
    try:
        f = open(scriptpath)
    except:
        return VerifiedResult(
            False,
            (
                f'Could not open file "{scriptname}". It might not exist or '
                "it might be in an unexpected location."
            ),
        )
    lines = [line.strip() for line in f.readlines()]
    try:
        f.close()
    except:
        pass
    q = "(\"|')"
    pattern = re.compile(f"^commit\\s*=\\s*{q}[0-9a-f]+{q}$")
    commits = set(
        line.split("=")[1].strip()[1:-1]
        for line in lines
        if pattern.fullmatch(line)
    )
    if len(commits) != 1:
        return VerifiedResult(
            False,
            "Could not determine what commit was used in the script.",
        )
    if list(commits)[0] != "a0ba5c3a6a5e0271ef9860ea8a5f8b73fce0e44d":
        return VerifiedResult(
            False,
            "This is not the commit associated with the Zenodo record.",
        )

    # Run the script
    out = subprocess.run(
        ["python3", scriptname],
        cwd=dir_lab,
        capture_output=True,
        text=True,
    )
    if out.returncode:
        return VerifiedResult(
            False,
            "Error when running the script: ." + out.stdout[:-1].split("\n"),
        )

    # Verify that the correct file was downloaded
    if not os.path.exists(datapath):
        return VerifiedResult(
            False,
            (
                f'File "{dataname}" has not been downloaded by the script or '
                "it has been downloaded in an unexpected location."
            ),
        )
    out = subprocess.run(
        ["sha256sum", datapath],
        capture_output=True,
        text=True,
    )
    if out.returncode:
        return VerifiedResult(
            False,
            (
                f"Error getting checksum of f{dataname}: ."
                + out.stdout[:-1].split("\n")
            ),
        )
    check = "9965ffde14e5b2afd01a78c752dc15a18e13cdb0819f77727b36b7cedcb7d8f9"
    if out.stdout[:-1].split("\n")[0].split()[0] != check:
        return VerifiedResult(
            False,
            "The downloaded data file is not the correct one.",
        )

    # If we reach this point, everything went well
    return VerifiedResult(True, None)


verifiers.append(
    Verifier(
        "Push gitignore file and script that downloads data",
        verify_download_data,
    )
)

# ---------------------------- #
# Run checks on the entire lab #
# ---------------------------- #


verify_lab(verifiers)
