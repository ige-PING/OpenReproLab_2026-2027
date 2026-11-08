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

from orlcitools import VerifiedResult, Verifier, path_of_repo, verify_lab

dir_lab = os.path.join(
    path_of_repo(),
    "labs",
    "01_ABC-of-repro-numerical-science",
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
        result = VerifiedResult(
            False,
            (
                f'Could not open file "{filename}". It might not exist or '
                "it might be in an unexpected location."
            ),
        )
    else:
        content = f.read()
        for c in " \t\n!-_":
            content = content.replace(c, "")
        if content.lower() == "welcometoopenreprolab":
            result = VerifiedResult(True, None)
        else:
            result = VerifiedResult(
                False,
                f'File "{filename}" was found but its content is incorrect.',
            )
    try:
        f.close()
    except:
        pass
    return result


verifiers.append(
    Verifier(
        'Push "Hello World" file to Github/Gitlab from command-line',
        verify_hello_world,
    )
)


# ---------------------------- #
# Run checks on the entire lab #
# ---------------------------- #


verify_lab(verifiers)
