This content is released under the terms of the [Creative Commons Attribution Share Alike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/).

# Lab 01: ABC of reproducible numerical science

## Configure git and Github/Gitlab authentication

Your first tasks are to:

 - Configure Git on your platform
 - Configure authenticated access to Github or Gitlab via the command-line.

To do so, follow [these instructions](./setting-up-git-github-gitlab.md).

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

First, create a text file named "hello-world.txt" that contains the text "Welcome to OpenReproLab!". This file must be located in lab 01's directory.

> [!TIP]
> Now is a good time to practice using `less` and `cat` to view the content of the file you just created.

Now onto the fun part: using the command-line, you will add this file to your Git repository and send it to Github/Gitlab. This process is akin to sending remote-sensing equipment into orbit, which is, as we all know, a four-step process:

 1. Make a list of all the equipment you have and that is not already in the spaceship.
 2. Load the relevant equipment into the spaceship.
 3. Lock the door of the spaceship when you are sure it is ready.
 4. Send the spaceship into orbit.

**1. List equipment:** Use to the command `git status` to list all the files that are not currently added to your Git repository. Your new file "hello-world.txt" should be listed in the _Untracked files_ section.

**2. Load equipment in spaceship:** Use the command `git add /path/to/file` to mark a given file as "ready to be committed" to the spaceship. Once done, feel free to use the `git status` command again to make sure that your "hello-world.txt" file is indeed listed in the _Changes to be committed_ section.

**3. Lock the door:** Use the command `git commit -m "Some useful information about the mission"` to tell Git that you have made up your mind and that the ship is ready for launch.

**4. Lauch spaceship into orbit:** Use the command `git push -u origin` to send to local changes to Github/Gitlab. Note that from now on, you can simply use `git push` for any further push to Github/Gitlab.

You can now use your web browser to make sure that your file has been properly uploaded to Github/Gitlab.

## Check that the previous part was done correctly

In OpenReproLab, we created a mechanism that automatically verifies that your lab work is correct.

## Create Python script that downloads CSV data

The aim of this section is to show how data can be downloaded from the Internet using scripts, as opposed to using a web browser.

We will download the file `data/processed/obs_evangelou2026-revised.csv` from the Zenodo record [GEOS-Chem-IGE/hough2026_atmo-plast-emis_harmonize: v1.0.1](https://zenodo.org/records/23046811). This file contains measurements of atmospheric concentrations of microplastics.

Try to think why it might be better to use a script rather than a web browser to download data from the Internet.

## Add function that calculates something on the data

## Move functions to Python module and use it from script

## Create Jupyter notebook that uses module

## To go a bit further

TODO: git log, commit hash, find the previous version of a file
