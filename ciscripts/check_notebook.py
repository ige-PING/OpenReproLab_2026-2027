"""Tools to handle notebooks in OpenReproLab 2026-2027 CI scripts.

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

import json
import sys
import re
import os
from pathlib import Path


def notebook(filepath):
        """Openning ta notebook as a json file
    
        Parameters
        ----------
        filepath: str
            Path to the notebook file
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            notebook = json.load(f)

        return notebook

def extract_all_code_cells(notebook):
        """Extract content of all code cells 
        from a notebook file

        Parameters
        ----------
        notebook: dict
            Content of a notebook open as a json file
        """
        output_lines = []
        source_lines = []
        for i, cell in enumerate(notebook.get('cells', []), 1):
            # Extract cell content
            cell_type = cell.get('cell_type', [])
            if cell_type == 'code':
                cell_output = cell.get('outputs', [])
                output_lines.append(cell_output)  
                cell_source = cell.get('source', [])
                source_lines.append(cell_source) 
    
        return source_lines, output_lines

def extract_all_raw_cells(notebook):
        """Extract content of all raw cells 
        from a notebook file

        Parameters
        ----------
        notebook: dict
            Content of a notebook open as a json file
        """
        output_lines = []
        source_lines = []
        for i, cell in enumerate(notebook.get('cells', []), 1):
            # Extract cell content
            cell_type = cell.get('cell_type', [])
            if cell_type == 'raw':
                cell_output = cell.get('outputs', [])
                output_lines.append(cell_output)  
                cell_source = cell.get('source', [])
                source_lines.append(cell_source) 
    
        return source_lines, output_lines

def check_answers_output(output_answer, output_correct):
        """Compare the output of one cell between two notebooks 

        Parameters
        ----------
        output_answer: list
            The output of one cell of notebook containing the answer 
        output_correct: list
            The output of one cell of notebook containing the correct answer 


        Returns
        -------
        bool
            True if the two are equal
        """

        if output_answer[0]['text'] == output_correct[0]['text']:
            return True
        else:
            return False

def check_answers_content(content_answer, content_correct):
        """Compare the content of one cell between two notebooks :
        the answer notebook must contain a string with the keywords defined
        in the answer notebook to be considered correct
        

        Parameters
        ----------
        content_answer: list
            The content of one cell of notebook containing the answer 
        content_correct: list
            The content of one cell of notebook containing the correct answer 


        Returns
        -------
        bool
            True if the content answer contains the key words defined in content_correct
        """

        answer = content_answer[0]
        keywords = content_correct[0].split()

        check = True
        for key in keywords:
            if not key in answer:
                check = False
        return check

def check_file_presence(filepath):
        """Check the presence of one particular file
        

        Parameters
        ----------
        filepath: str
            Path to file

        Returns
        -------
        bool
            True if the file exists, False if not
        """

        return os.path.exists(filepath)
        
def check_answers(list_questions, notebook1, notebook2, path_of_repo):
        """Check answers in a notebook versus correct answers.

        Parameters
        ----------
        list_questions: list
            The number of the question, the type of cell it requires and either the position in the notebook 
            list of cells or path to a file. The required format is:

            [
                ("1.1", raw, 0),
                ("3.2", code, 3),
                ("5.1", file, "path_to_file"),
                ...
            ]


        Returns
        -------
        bool
            True if and only if all questions were answered correctly.

        Prints
        ------
        Information on each question: the title and whether the question was answered
        correctly or not

        """

        source_raw_cell_lines, output_raw_cell_lines = extract_all_raw_cells(notebook1)
        source_code_cell_lines, output_code_cell_lines = extract_all_code_cells(notebook1)
        answer_source_raw_cell_lines, answer_output_raw_cell_lines = extract_all_raw_cells(notebook2)
        answer_source_code_cell_lines, answer_output_code_cell_lines = extract_all_code_cells(notebook2)

        all_check = True
    
        for i_questions, question in enumerate(list_questions):
            title, typeq, nb = list_questions[i_questions]

            check = True
            
            if typeq == "code":
                if not check_answers_output(output_code_cell_lines[nb],answer_output_code_cell_lines[nb]):
                    check = False

            if typeq == "raw":
                if not check_answers_content(source_raw_cell_lines[nb],answer_source_raw_cell_lines[nb]):
                    check = False

            if typeq == "file":
                if not check_file_presence(nb):
                    check = False

            if check == True:
                print("Answer to question "+title+" is correct.")
            else:
                print("Answer to question "+title+" is incorrect.")  
                all_check = False

        return all_check

        
        