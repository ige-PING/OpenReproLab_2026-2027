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

from misctools import part_banner, path_of_repo, check_url_zenodo_sandbox
from questionnaire import Questionnaire
from check_notebook import *

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
all_good_part1 = questionnaire.check_answers(
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
# Part 2: Data format #
# ---------------------------------------------#

part_banner(2, "Data format")

data_format_notebook = notebook(
    os.path.join(
        path_of_repo(),
        "labs",
        "02_data-management",
        "data-format.ipynb",
    )
)

answers_data_format_notebook = notebook(
    os.path.join(
        path_of_repo(),
        "ciscripts",
        "data-format-answers.ipynb",
    )
)

all_good_part2 = check_answers(
    [
        ("1.1","code",0),
        ("1.2","code",1),
        ("1.3","raw",0),
        ("1.4","code",2),
        ("1.5","file","data/newprecip.txt"),
        ("1.6","raw",1),
        ("2.1","code",3),
        ("2.2","code",4),
        ("2.3","code",5),
        ("2.4","file","data/new_precipitation.csv"),
        ("2.5","raw",2),
        ("3.1","code",6),
        ("3.2","code",7),
        ("3.3","code",8),
        ("3.4","code",9),
        ("3.5","code",10),
        ("3.6","file","data/random_temp_press.nc"),
        
    ],
   data_format_notebook, answers_data_format_notebook, path_of_repo() 
)

   
# ---------------------------------------------#
# Part 3: Data Warehouses                      #
# ---------------------------------------------#

part_banner(3, "Upload of data on zenodo sandbox")

upload_success = check_url_zenodo_sandbox(
    os.path.join(
        path_of_repo(),
        "labs",
        "02_data-management",
        "zenodo-sandbox-link.md",
    )
)

if all_good_part1 && all_good_part2 && upload_success:
    print("Lab 02 completed succesfully, congratulations!")
    sys.exit(0)
else:
    print("Some checks failed, keep at it!")
    sys.exit(1)
