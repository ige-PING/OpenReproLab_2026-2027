import os
import subprocess

def download_file_from_github(
    repository = "GEOS-Chem-IGE/hough2026_atmo-plast-emis_harmonize",
    commit = "a0ba5c3a6a5e0271ef9860ea8a5f8b73fce0e44d",
    filepath = "data/processed/obs_evangelou2026-revised.csv",
    ) -> None:
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
