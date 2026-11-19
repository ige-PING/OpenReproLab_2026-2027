import requests
import urllib.parse
import subprocess


def download_file_from_github(repository: str, commit: str, filepath: str):
    """Download specific file from Github repository.

    Parameters
    ----------
    repository: str
        Name of the repository.
    commit: str
        Commit of interest (full hash).
    filepath: str
        File of interest within repository.
    """

    BASE_URL = "https://raw.githubusercontent.com"

    # Download the file using wget
    url = urllib.parse.urljoin(BASE_URL, "/".join((repository, commit, filepath)))
    out = subprocess.run(["wget", url], capture_output=True, text=True)
    if out.returncode:
        msg = out.stderr
        raise RuntimeError(msg)
