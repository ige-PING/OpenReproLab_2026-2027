"""Miscellaneous tools for OpenReproLab 2026-2027 CI scripts.

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
from collections import namedtuple

VerifiedResult = namedtuple("VerifiedResult", "ok feedback")


def path_of_repo(path=None):
    """Return path of Git repository containing given path.

    Parameters
    ----------
    path: str
        A path that is supposed to be located somewhere in a Git repository. If
        None, then this function returns the path of the Git repository
        containing this module.

    Returns
    -------
    str
        The path of the Git repository that contains given path.

    Notes
    -----
    Given path does not have to exist to find the corresponding Git repository.
    For example, if /home/myself/myrepo is an existing Git repository, then
    path_of_repo("/home/myself/myrepo/myfile.txt") will return
    "/home/myself/myrepo" even if myfile.txt does not exists.

    """
    abspath = os.path.abspath(__file__ if path is None else path)
    if os.path.isdir(os.path.join(abspath, ".git")):
        return abspath
    parent = os.path.dirname(abspath)
    if parent == abspath:
        msg = "Could not determine path to git repository."
        raise RuntimeError(msg)
    else:
        return path_of_repo(parent)


def print_banner(name):
    """Print a banner, typically to indicate the part of the lab being checked.

    Parameters
    ----------
    name: str
        The name of the part.

    """
    middle_line = f"# {name} #"
    around_line = "-" * (len(middle_line) - 2)
    print(f"\n#{around_line}#\n{middle_line}\n#{around_line}#\n")


class Verifier:
    """Represent and run a verification check for one part of a lab.

    Parameters
    ----------
    title: str
        The title of the part to be verified.
    verify_function: function
        The function that will be called to verify the part. This function
        should return a VerifiedResult instance.

    """

    def __init__(self, title, verify_function):
        self.title = title
        self.verify_function = verify_function

    def verify(self):
        """Run verification and print feedback.

        Returns
        -------
        VerifiedResult
            The outcome of the verification.

        """
        print_banner(self.title)
        result = self.verify_function()
        if result.feedback is not None and result.feedback.strip() != "":
            print(result.feedback)
            print()
        if result.ok:
            print("Part completed successfully!")
        else:
            print("Some checks failed for this part, try again!")
        return result.ok


def verify_lab(verifiers):
    """Run and report the verification checks for each lab part.

    This function should be called at the end of each lab script.

    Parameters
    ----------
    Verifiers: list[Verifier]
        The list of verifiers for the lab.

    """
    results = [verifier.verify() for verifier in verifiers]
    print_banner("Summary for the entire lab")
    if all(results):
        print("==> Lab completed succesfully, congratulations!")
        sys.exit(0)
    else:
        print("==> Some checks failed, keep at it!")
        sys.exit(1)


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
            lines = [line.strip() for line in f]
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
            elif line.startswith(start_s) or line.startswith(start_s.upper()):
                self.questions[-1].add_choice(line[len(start_s) :], True)
            else:
                msg = f"Could not parse line {i_line + 1}: {line}."
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
