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

    import os
    import subprocess

    base_url = "https://raw.githubusercontent.com"

    #if __name__ == "__main__":
    # Remove target file if already present
    print("start downloading function:")
    try:
        os.remove(os.path.basename(filepath))
        print(f"Removed existing file: {os.path.basename(filepath)}")
    except:
        pass

    # Download the file using wget
    url = "/".join([base_url, repository, commit, filepath])
    print(url)
    out = subprocess.run(["wget", url], capture_output=True, text=True)
    if out.returncode:
        msg = out.stderr
        raise RuntimeError(msg)
    print(f"Downloaded file: {os.path.basename(filepath)}")
