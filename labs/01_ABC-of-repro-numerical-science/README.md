This content is released under the terms of the [Creative Commons Attribution Share Alike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/).

# Lab 01: ABC of reproducible numerical science

## Configure git and Github/Gitlab authentication

Follow [these instructions](./setting-up-git-github-gitlab.md) to:

 - Configure Git on your platform
 - Configure authenticated access to Github or Gitlab via the command-line.

## Clone OpenReproLab repository

Now that Git is properly configured, you can clone the OpenReproLab repository on your machine:

```sh
# You can clone it from Github...
git clone git@github.com:ige-PING/OpenReproLab_2026-2027.git

# ... or from Gricad's Gitlab
git clone git@gricad-gitlab.univ-grenoble-alpes.fr:ping/openreprolab_2026-2027.git

# Move to the OpenReproLab directory
cd openreprolab_2026-2027
```

If you are an OpenReproLab student, run the following commands (replace `${username}` by your Github or Gitlab username):

```sh
git branch user/${username} origin/user/${username}
git checkout user/${username}
```

> [!NOTE]
> We do not explain what these last commands do, please bear with us here :smiley: :bear:. Suffice it to say that this allows each OpenReproLab student to work without interfering with others. This is a first-time setup: you will not have to run these commands every time.

## Push "Hello World" file to Github/Gitlab from command-line

This first exercise aims to teach you the basics of using Git and Github/Gitlab.

First, create a text file named `hello-world.txt` that contains the text "Welcome to OpenReproLab!". This file must be located in lab 01's directory.

> [!TIP]
> Now is a good time to practise using `less` and `cat` to view the content of the file you just created.

Now onto the fun part: using the command-line, you will add this file to your Git repository and send it to Github/Gitlab. This process is akin to sending remote-sensing equipment into orbit, which is, as we all know, a four-step process:

 1. Make a list of all the equipment you have and that is not already in the spaceship.
 2. Load the relevant equipment into the spaceship.
 3. Lock the door of the spaceship when you are sure it is ready.
 4. Send the spaceship into orbit.

**1. List equipment:** Use to the command `git status` to list all the files that are not currently added to your Git repository. Your new file `hello-world.txt` should be listed in the _Untracked files_ section.

**2. Load equipment in spaceship:** Use the command `git add /path/to/file` to mark a given file as "ready to be committed" to the spaceship. Once done, feel free to use the `git status` command again to make sure that your `hello-world.txt` file is indeed listed in the _Changes to be committed_ section.

**3. Lock the door:** Use the command `git commit -m "Some useful information about the mission"` to tell Git that you have made up your mind and that the ship is ready for launch.

**4. Lauch spaceship into orbit:** Use the command `git push -u origin` to send to local changes to Github/Gitlab. Note that from now on, you can simply use `git push` for any further push to Github/Gitlab.

You can now use your web browser to make sure that your file has been properly uploaded to Github/Gitlab.

> [!IMPORTANT]
> In this section you have learned:
> - How to clone a repository from Github/Gitlab
> - How to add a file to a local repository (add and commit)
> - How to send your updating repository to Github/Gitlab (push)

## Check that the previous part was done correctly

In OpenReproLab, we created a mechanism that automatically verifies that your lab work is correct. So let us go find out now if you did the previous part correctly!

To do so, use your web browser to navigate to the OpenReproLab repository on Github, then click on _Actions_ (located towards the top of the page).

You will be presented with a long list of so-called workflow results. To only display relevant results, Click on "Lab01" in the left-hand-side column, then filter the list to only show workflows that have been ran on your branch (`user/${username}`).

You should now see that a workflow named `Lab01` has been run on your latest commit. A green tick icon will indicate that all parts of Lab01 have been completed successfully.

This cannot yet be the case however, because you have only worked on the first part so far. You should therefore see a red-cross mark. Click on the workflow and explore the logs to see whether you successfully completed part 1.

If you did not succeed, go back to the previous part, modify `hello-world.txt` accordingly, and send your changes to Github/Gitlab using the `add`-`commit`-`push` workflow until you succeed.

> [!IMPORTANT]
> In this section you have learned:
> - How to check the outputs of our lab-checking facilities

## Create Python script that downloads CSV data

As a preliminary exercise, run the `git log` command from inside your repository and try to make sense of what you see by answering the following questions for yourself (ask a peer or an instructor for explanations if needed):

 - What is a commit?
 - What is a commit hash?
 - Who made these other commits that you are seeing?

The goal of this section is to show how data can be downloaded from the Internet using scripts, as opposed to using a web browser. We aim to show that using scripts is more reproducible.

For this exercise, you will download the file corresponding to `data/processed/obs_evangelou2026-revised.csv` from the Zenodo record [GEOS-Chem-IGE/hough2026_atmo-plast-emis_harmonize: v1.0.1](https://zenodo.org/records/23046811). This file contains measurements of atmospheric concentrations of microplastics.

To do so:

 - Modify the script `download-micro-plastics-data.py` as necessary (read comments for more information).
 - Run the script using `python3 download-micro-plastics-data.py`.
 - Verify that the file has been downloaded and take a look inside it.

Try to think of at least three reasons why it might be better to use a script rather than a web browser to download data from the Internet.

Also, why is it important for reproducibility to specify explicitly which commit we want to download the data from?

> [!IMPORTANT]
> In this section you have learned:
> - How to modify an existing Python script
> - How to run a Python script
> - How to use Python to download a specific file from Github

## Add this script to Github/Gitlab without adding the data itself

Now that the script seems to be working, we want to commit it and send it to GitHub/Gitlab.

If you run `git status`, you should see that:

 - There is a new untracked file called `obs_evangelou2026-revised.csv`. It is the file that the script downloaded.
 - Git knows that the file `download-micro-plastics-data.py` has been modified.

We want to commit the modified script but **not** the CSV data file. These data are already available from Github and we do not want to create unnecessary entropy by duplicating them. We will therefore tell Git that this file should not be tracked. To do that, create a file name `.gitignore` in lab 01's directory with the following content:

```
# Ignore the data file downloaded by the script
obs_evangelou2026-revised.csv
```
Run `git status` again to make sure that Git now ignores this file.

As mentionned before, Git has noticed that you have modified the Python script. Use `git diff download-micro-plastics-data.py` to review your changes. Once you are satisfied with your changes: add, commit, and push both the `.gitignore` file and the modified script. Make sure your work passes our tests for this section before moving on to the next one.

> [!IMPORTANT]
> In this section you have learned:
> - How to create `.gitignore` files to prevent tracking unwanted files
> - How to use `git diff` to see ongoing modifications
> - How to commit and push modified files

## Create a Jupyter notebook that plots microplastics data

## Multiple-choice quizz on what you learned in this lab
