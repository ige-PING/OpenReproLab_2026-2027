"""Script to check answers of lab 04 of OpenReproLab 2026-2027.

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

from misctools import part_banner, path_of_repo
from questionnaire import Questionnaire

# -----------------------------------#
# Part 1: Questionnaire on licenses #
# -----------------------------------#

part_banner(1, "Questionnaire on licenses")

questionnaire = Questionnaire(
    os.path.join(
        path_of_repo(),
        "labs",
        "04_code-management-01",
        "questionnaire-on-licenses.md",
    )
)
questionnaire.check_answers(
    [
        [
            [1],
            (
                "Software is protected by copyright law, so usage is "
                "restricted if no license is provided, even if the code is "
                "publicly available. A suitable license may give users "
                "additional permissions and make the software free and open "
                "source."
            ),
        ],
        [
            [0, 2, 3, 4],
            (
                "With very few exceptions, you must always give proper credit "
                "when you re-distribute free and open-source software. In no "
                "circumstances it is ethical to claim you created something "
                "that was created by someone else. Most free and open-source "
                "software licenses allow you to sell the source code (or "
                "services related to the software) under certain conditions. "
                "You must accept however that users may decide to obtain the "
                "software for free from the Internet or from someone else who "
                "already has a copy of it."
            ),
        ],
    ]
)
