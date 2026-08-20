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
        self.choices = []

    def add_choice(self, choice, selected):
        """Add a possible choice to self.

        Parameters
        ----------
        choice: str
            The text of the choice.
        selected: bool
            Whether the choice was selected in the questionnaire.

        """
        self.choices.append(Choice(choice, selected))

    def __repr__(self):
        """String representation of self."""
        out = f"{self.question}\n"
        if len(self.choices) > 0:
            out += "\n"
        out += "\n".join(str(choice) for choice in self.choices)
        return out + "\n"


class Choice:
    """Class that represents one of the multiple choices of a question."""

    def __init__(self, choice, selected):
        """Initialize self.

        Parameters
        ----------
        choice: str
            The text of the choice.
        selected: bool
            Whether the choice was selected in the questionnaire.

        """
        self.choice = choice.strip()
        self.selected = bool(selected)

    def __repr__(self):
        """String representation of self."""
        mark = "x" if self.selected else " "
        return f" - [{mark}] {self.choice}"


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
                self.questions[-1].add_choice(line[len(start_a) :], False)
            elif line.startswith(start_s):
                self.questions[-1].add_choice(line[len(start_s) :], True)
            else:
                msg = f"Could not parse line {i_line}: {line}."
                raise ValueError(msg)

    def __repr__(self):
        """String representation of self."""
        return "\n".join(f"{i + 1}. {q}" for i, q in enumerate(self.questions))

    def check_answers(self, correct_answers):
        """Check choices selected in questionnaire versus correct answers.

        Parameters
        ----------
        correct_answers: list
            The correct answers, along with hints to help students find the
            correct answers. The required format is:

            [
                ([0], "Hint for question 1"),
                ([2, 4], "Hint for question 2"),
                ...
            ]

            where the numbers are the 0-based indices of the correct choices.

        Returns
        -------
        bool
            True if and only if all questions were answered correctly.

        Prints
        ------
        Information on each question: whether the question was answered
        correctly and, if not, the corresponding hint.

        """
        if len(correct_answers) != len(self.questions):
            msg = "Incorrect number of answers."
            raise ValueError(msg)

        questionnaire_is_correct = True
        for i_question, question in enumerate(self.questions):
            correct, hint = correct_answers[i_question]

            if min(correct) < 0 or max(correct) > len(question.choices) - 1:
                msg = "Bad index value (too small or too large)."
                raise ValueError(msg)

            question_is_correct = True
            for i_choice, choice in enumerate(question.choices):
                if choice.selected and i_choice in correct:
                    # Correct positive answer
                    pass
                elif not choice.selected and i_choice not in correct:
                    # Correct negative answer
                    pass
                else:
                    question_is_correct = False
                    questionnaire_is_correct = False
                    break

            # Print feedback
            if question_is_correct:
                print(f"Answer to question {i_question + 1} is correct.\n")
            else:
                print(f"Answer to question {i_question + 1} is incorrect.\n")
                if len(hint.strip()) > 0:
                    print(f"Hint: {hint}\n")

        return questionnaire_is_correct
