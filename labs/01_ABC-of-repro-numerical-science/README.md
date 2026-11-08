This content is released under the terms of the [Creative Commons Attribution Share Alike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/).

# Lab 01: ABC of reproducible numerical science

## Configure git and Github/Gitlab authentication

Your first task is to configure Git on your platform, as well as authenticated access to Github or Gitlab via the command-line.

To do so, follow [these instructions](./setting-up-git-github-gitlab.md).

## Clone OpenReproLab repository

Now that Git is properly configured, you can clone the OpenReproLab repository on your machine:

```sh
# From Github
git clone git@github.com:ige-PING/OpenReproLab_2026-2027.git

# Or Gitlab
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

## Push "Hello world" file to Github/Gitlab from command-line

## Create Python script that downloads CSV data

The aim of this section is to show how data can be downloaded from the Internet using scripts, as opposed to using a web browser.

We will download the file `data/processed/obs_evangelou2026-revised.csv` from the Zenodo record [GEOS-Chem-IGE/hough2026_atmo-plast-emis_harmonize: v1.0.1](https://zenodo.org/records/23046811). This file contains measurements of atmospheric concentrations of microplastics.

Try to think why it might be better to use a script rather than a web brower to download data from the Internet.

## Add function that calculates something on the data

## Move functions to Python module and use it from script

## Create Jupyter notebook that uses module

## To go a bit further

TODO: git log, commit hash, find the previous version of a file
