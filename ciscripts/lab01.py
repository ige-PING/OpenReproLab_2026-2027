"""Script to check answers of lab 01 of OpenReproLab 2026-2027.

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
import os
import re
import subprocess

import orlcitools

dir_repo = orlcitools.path_of_repo()
dir_lab = os.path.join(dir_repo, "labs", "01_ABC-of-repro-numerical-science")
dir_ciscripts = os.path.join(dir_repo, "ciscripts")
could_not_open_file = (
    'Could not open file "%s". It might not exist or it '
    "might be in an unexpected location."
)
VerifiedResult = orlcitools.VerifiedResult
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
    orlcitools.Verifier(
        'Push "Hello World" file to Github/Gitlab from command-line',
        verify_hello_world,
    )
)


# --------------------------- #
# Download microplastics data #
# --------------------------- #

dataname = "obs_evangelou2026-revised.csv"
datapath = os.path.join(dir_lab, dataname)

ignorename = ".gitignore"
ignorepath = os.path.join(dir_lab, ignorename)

scriptmodule = "download_microplastics_data"
scriptname = f"{scriptmodule}.py"
scriptpath = os.path.join(dir_lab, scriptname)


def verify_csv_no_data_file():
    """Verifier function for the data-downloading part (no csv file)."""
    return orlcitools.verifier_function_is_absent(datapath)


def verify_csv_gitignore():
    """Verifier function for the data-downloading part (.gitignore)."""
    try:
        f = open(ignorepath)
    except:
        return VerifiedResult(False, could_not_open_file % ignorename)
    lines = [line.strip() for line in f]
    try:
        f.close()
    except:
        pass
    accepted = (dataname, f"./{dataname}", "*.csv", "**/*.csv")
    if all(line not in accepted for line in lines):
        return VerifiedResult(
            False,
            f'Missing rule to ignore "{dataname}" in ".gitignore".',
        )
    return VerifiedResult(True, None)


def verify_csv_commit_is_correct():
    """Verifier function for the data-downloading part (correct commit)."""
    # Remove module file(s) that could be imported instead of the correct one
    try:
        os.remove(os.path.join(dir_ciscripts, scriptname))
    except:
        pass

    # Get the commit hash that is coded in the script
    python_code = [
        f"import {scriptmodule}",
        f"print({scriptmodule}.commit)",
    ]
    out = subprocess.run(
        ["python3", "-c", "\n".join(python_code)],
        cwd=dir_lab,
        capture_output=True,
        text=True,
    )
    if out.returncode:
        return VerifiedResult(
            False,
            (
                "I encountered a problem when trying to read "
                f'the commit information from "{scriptname}". '
                f"The error message was:\n\n{out.stderr}"
            ),
        )
    commit = out.stdout[:-1].split("\n")[0]
    if commit != "a0ba5c3a6a5e0271ef9860ea8a5f8b73fce0e44d":
        return VerifiedResult(
            False,
            (
                f"{scriptname}: This is not the commit associated "
                "with the Zenodo record."
            ),
        )
    return VerifiedResult(True, None)


def verify_csv_download_works():
    """Verifier function for the data-downloading part (test script)."""
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
            (
                "Error when running the script. "
                f"The error message was:\n\n{out.stderr}"
            ),
        )

    # Verify that the correct file was downloaded
    result = orlcitools.verifier_function_checksum(
        datapath,
        "9965ffde14e5b2afd01a78c752dc15a18e13cdb0819f77727b36b7cedcb7d8f9",
        msg_if_failed="The downloaded data file is not the correct one.",
    )
    if not result.success:
        return result

    # If we reach this point, everything went well
    return VerifiedResult(True, None)


verifiers.append(
    orlcitools.Verifier(
        "Push script that downloads data and gitignore file",
        [
            verify_csv_no_data_file,
            verify_csv_gitignore,
            verify_csv_commit_is_correct,
            verify_csv_download_works,
        ],
    )
)


# --------------------------- #
# Jupyter notebook, no module #
# --------------------------- #


notebookname = "analyse_microplastics.ipynb"
notebookpath = os.path.join(dir_lab, notebookname)


def verify_notebook_nomodule_gitignore():
    """Verifier function for the Jupyter notebook part (.gitignore)."""
    try:
        f = open(ignorepath)
    except:
        return VerifiedResult(False, could_not_open_file % ignorename)
    lines = [line.strip() for line in f]
    try:
        f.close()
    except:
        pass
    accepted = (
        ".ipynb_checkpoints",
        ".ipynb_checkpoints/",
        ".ipynb_checkpoints/*",
    )
    if all(line not in accepted for line in lines):
        return VerifiedResult(
            False,
            'Missing rule to ignore ".ipynb_checkpoints" in "gitignore."',
        )
    return VerifiedResult(True, None)


def verify_notebook_nomodule_notebook():
    """Verifier function for the Jupyter notebook (without using a module)."""
    try:
        f = open(notebookpath)
    except:
        return VerifiedResult(False, could_not_open_file % notebookpath)
    notebook_json = f.read()
    try:
        f.close()
    except:
        pass
    try:
        notebook = json.loads(notebook_json)
    except:
        return VerifiedResult(False, "Could not parse the notebook.")

    # We verify that:
    # - The averages are correctly calculated
    # - The notebook contains two figures
    expected_line1 = (
        "Average atmospheric microplastics composition = 45 particles/m3\n"
    )
    expected_line2 = (
        "Average microplastics deposition rate = 169 particles/m2/d\n"
    )
    averages_ok = False
    n_figures = 0
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        try:
            outputs = cell["outputs"]
        except:
            continue

        # Detect figures
        for output in outputs:
            try:
                n_figures += "image/png" in output["data"]
            except:
                pass

        # Detect the calculation of averages
        try:
            output_name = outputs[0]["name"]
            output_type = outputs[0]["output_type"]
            line1, line2 = output["text"]
        except:
            pass
        else:
            if output_name == "stdout" and output_type == "stream":
                if line1 == expected_line1 and line2 == expected_line2:
                    averages_ok = True

    # Conclude
    msg = ""
    if n_figures < 2 and not averages_ok:
        msg = (
            "Two figures are expected, and the averages are "
            "missing or incorrect."
        )
    elif not averages_ok:
        msg = "The averages are missing or incorrect."
    elif n_figures < 2:
        msg = "Two figures are expected."
    return VerifiedResult(msg == "", msg)


verifiers.append(
    orlcitools.Verifier(
        "Create notebook and update gitignore file",
        [
            verify_notebook_nomodule_gitignore,
            verify_notebook_nomodule_notebook,
        ],
    )
)


# ----------------------------- #
# Jupyter notebook, with module #
# ----------------------------- #


modulename = "lab01utils"
modulepath = os.path.join(dir_lab, f"{modulename}.py")
data_dl_function_name = "download_file_from_github"


def verify_notebook_module_test_module():
    """Verifier function for the Jupyter notebook (test the module)."""
    # Remove module file(s) that could be imported instead of the correct one
    try:
        os.remove(os.path.join(dir_ciscripts, os.path.basename(modulepath)))
    except:
        pass

    # Check that the module file exists
    if not os.path.isfile(modulepath):
        return VerifiedResult(
            False,
            (
                f'Module file "{os.path.basename(modulepath)}" could not '
                "be found or it is a directory instead."
            ),
        )

    # Test the module
    out = subprocess.run(
        ["python3", "lab01_test-module-that-downloads-github-files.py"],
        cwd=dir_ciscripts,
        capture_output=True,
        text=True,
    )
    if out.returncode:
        return VerifiedResult(
            False,
            (
                f'Problem when testing function "{data_dl_function_name}". '
                f"The error message was:\n\n{out.stderr}"
            ),
        )

    # If we reach this point, everything went well
    return VerifiedResult(True, None)


def verify_notebook_module_notebook():
    """Verifier function for the Jupyter notebook (using a module)."""
    try:
        f = open(notebookpath)
    except:
        return VerifiedResult(False, could_not_open_file % notebookpath)
    notebook_json = f.read()
    try:
        f.close()
    except:
        pass
    try:
        notebook = json.loads(notebook_json)
    except:
        return VerifiedResult(False, "Could not parse the notebook.")

    # We verify that:
    # - The import statement is found
    # - The function is called
    import_ok = False
    function_ok = False
    import_valid = (
        f"import {modulename}",
        f"from {modulename} import {data_dl_function_name}",
    )
    function_valid = (
        re.compile(f"^{data_dl_function_name}\\s*\\("),
        re.compile(f"^{modulename}.{data_dl_function_name}\\s*\\("),
    )

    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        try:
            source = cell["source"]
        except:
            continue

        for line in source:
            strip = line.strip()
            if any(strip.startswith(v) for v in import_valid):
                import_ok = True
            if any(v.match(strip) is not None for v in function_valid):
                function_ok = True

    # Conclude
    msg = ""
    if not import_ok and not function_ok:
        msg = (
            f'Module "{modulename}" is not imported in notebook and '
            f'function "{data_dl_function_name}" is not called.'
        )
    elif not import_ok:
        msg = f'Module "{modulename}" is not imported in notebook.'
    elif not function_ok:
        msg = f'Function "{data_dl_function_name}" is not called in notebook.'
    return VerifiedResult(msg == "", msg)


verifiers.append(
    orlcitools.Verifier(
        "Create module and use it in the notebook",
        [
            verify_notebook_module_test_module,
            verify_notebook_module_notebook,
        ],
    )
)


# ---------------------------- #
# Run checks on the entire lab #
# ---------------------------- #


if __name__ == "__main__":
    orlcitools.verify_lab(verifiers)
