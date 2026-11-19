import os
import subprocess

def download_file_from_github(repository, commit, filepath):
    """Download specific file from Github repository.

    Parameters
    ----------
    repository: str
        Name of the repository.
    commit: str
        Commit of interest (full hash).
    filepath
        File of interest within repository.

    """
    base_url = "https://raw.githubusercontent.com"

    if __name__ == "__main__":
    # Remove target file if already present
        try:
            os.remove(os.path.basename(filepath))
        except:
            pass

    # Download the file using wget
    url = "/".join([base_url, repository, commit, filepath])
    out = subprocess.run(["wget", url], capture_output=True, text=True)
    if out.returncode:
        msg = out.stderr
        raise RuntimeError(msg)
