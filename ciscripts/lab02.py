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

from misctools import part_banner, path_of_repo
from questionnaire import Questionnaire

# ---------------------------------------------#
# Part 1: Questionnaire on the FAIR principles #
# ---------------------------------------------#

part_banner(1, "Questionnaire on the FAIR principles")

questionnaire = Questionnaire(
    os.path.join(
        path_of_repo(),
        "labs",
        "02_data_management",
        "questionnaire-on-fair.md",
    )
)
all_good = questionnaire.check_answers(
    [
        [
            [0, 1, 2, 3, 4, 5],
            ("Go check https://www.nature.com/articles/sdata201618"),
        ],
        [
            [1],
            ("Go check https://www.gofair.foundation/fair-principles"),
        ],
        [
            [2],
            ("Go check https://www.gofair.foundation/fair-principles"),
        ],
        [
            [0],
            ("Go check https://www.gofair.foundation/fair-principles"),
        ],
        [
            [2],
            ("Go check https://www.gofair.foundation/fair-principles"),
        ],
        [
            [1, 2, 4],
            (
                "Interoperable data can be used and combined with other data, "
                "and can be manipulated natively by a variety of software."
            ),
        ],
        [
            [0, 1, 2, 3, 4, 5],
            (
                "To be reusable, datasets need to be thoroughly and clearly "
                "described, including how they were created, to increase "
                "transparency and trust. Datasets must also be licensed with "
                "a licence that permits reuse."
            ),
        ],
    ]
)

if all_good:
    print("Lab 02 completed succesfully, congratulations!")
    sys.exit(0)
else:
    print("Some checks failed, keep at it!")
    sys.exit(1)
