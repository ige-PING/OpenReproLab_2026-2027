"""Tools to handle questionnaires in OpenReproLab 2026-2027 CI scripts.

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


class Question:
    """Class to handle a single question, along with its multiple choices."""

    def __init__(self, question):
        """Initialize self.

        Parameters
        ----------
        question: str
            The text of the question.

        """
        self.question = question.strip()
        self.answers = []

    def add_answer(self, answer, selected):
        """Add a possible answer to self (ie. one of the multiple choices).

        Parameters
        ----------
        answer: str
            The text of the answer.
        selected: bool
            Whether the answer was selected in the questionnaire.

        """
        self.answers.append(Answer(answer, selected))

    def __repr__(self):
        """String representation of self."""
        out = f"{self.question}\n"
        if len(self.answers) > 0:
            out += "\n"
        out += "\n".join(str(answer) for answer in self.answers)
        return out + "\n"


class Answer:
    """Class that represents one of the multiple choices of a question."""

    def __init__(self, answer, selected):
        """Initialize self.

        Parameters
        ----------
        answer: str
            The text of the answer.
        selected: bool
            Whether the answer was selected in the questionnaire.

        """
        self.answer = answer.strip()
        self.selected = bool(selected)

    def __repr__(self):
        """String representation of self."""
        mark = "x" if self.selected else " "
        return f" - [{mark}] {self.answer}"


class Questionnaire:
    """Class to handle full questionnaires."""

    def __init__(self, filepath):
        """Initialize self by parsing a file.

        Parameters
        ----------
        filepath: str
            Path to the file containing the questionnaire.

        """
        self.questions = []
        with open(filepath) as f:
            lines = [line.strip() for line in f.readlines()]
        counter = 1
        for i_line, line in enumerate(lines):
            if len(line) == 0:
                continue
            start_q = f"{counter}. "
            start_a = "- [ ] "
            start_s = "- [x] "
            if line.startswith(start_q):
                self.questions.append(Question(line[len(start_q) :]))
                counter += 1
            elif line.startswith(start_a):
                self.questions[-1].add_answer(line[len(start_a) :], False)
            elif line.startswith(start_s):
                self.questions[-1].add_answer(line[len(start_s) :], True)
            else:
                msg = f"Could not parse line {i_line}: {line}."
                raise ValueError(msg)

    def __repr__(self):
        """String representation of self."""
        return "\n".join(f"{i + 1}. {q}" for i, q in enumerate(self.questions))
