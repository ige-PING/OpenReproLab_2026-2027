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
import sys

from misctools import part_banner, path_of_repo, check_url
from questionnaire import Questionnaire

# ---------------------------------------------#
# Part 1: Questionnaire on the FAIR principles #
# ---------------------------------------------#

part_banner(1, "Questionnaire on the FAIR principles")

questionnaire = Questionnaire(
    os.path.join(
        path_of_repo(),
        "labs",
        "02_data-management",
        "questionnaire-on-fair.md",
    )
)
all_good = questionnaire.check_answers(
    [
        [
            [0,1,2,3,4,5],
            (
                "Go check https://www.nature.com/articles/sdata201618"
            ),
        ],
        [
            [1],
            (
                "Go check https://www.gofair.foundation/fair-principles"
            ),
        ],
                [
            [2],
            (
                "Go check https://www.gofair.foundation/fair-principles"
            ),
        ],
                [
            [0],
            (
                "Go check https://www.gofair.foundation/fair-principles"
            ),
        ],
                [
            [2],
            (
                "Go check https://www.gofair.foundation/fair-principles"
            ),
        ],
                [
            [1,2,4],
            (
                "Interoperable means the data usually need to be integrated"
                "with other data. In addition, the data need to interoperate"
                "with applications or workflows for analysis, storage, and processing."
            ),
        ],
                [
            [0,1,2,3,4,5],
            (
                "Reusable describes data that can be used again, beyond its original purpose."
                "To be reusable, data not only needs to be described in a way to help others"
                "understand it, but also must be licensed with a licence that permits reuse."
                " Furthermore, data must contain information about how it was created - provenance"
                " - so that others know whether the data can be trusted"
            ),
        ],
    ]
)

   
# ---------------------------------------------#
# Part 3: Data Warehouses                      #
# ---------------------------------------------#

part_banner(3, "Upload of data on zenodo sandbox")

upload_success = check_url(
    os.path.join(
        path_of_repo(),
        "labs",
        "02_data-management",
        "zenodo-sandbox-link.md",
    )
)

if all_good && upload_success:
    print("Lab 02 completed succesfully, congratulations!")
    sys.exit(0)
else:
    print("Some checks failed, keep at it!")
    sys.exit(1)
