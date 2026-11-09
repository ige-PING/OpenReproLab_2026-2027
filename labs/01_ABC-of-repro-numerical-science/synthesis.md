# Synthesis: ABC of reproducible numerical science

## Reading and viewing list

 - Read [this introduction to open research](https://book.the-turing-way.org/reproducible-research/open/).
 - Then watch [this video](https://git-scm.com/video/what-is-version-control) that explains the basics of version control software such as Git, then read [this short complement](https://book.the-turing-way.org/reproducible-research/vcs/vcs-workflow/).
 - Wonder why this relates to open and reproducible science? Then [read this](https://book.the-turing-way.org/reproducible-research/vcs/).
 - Learn about the strength and limitations of using Git to do open science by reading [this](https://book.the-turing-way.org/reproducible-research/vcs/vcs-git-in-research/) (ignore the last section) and [this](https://book.the-turing-way.org/reproducible-research/vcs/vcs-git-general/).

## Git

Git is a very useful tool for every day research work: it helps keep track of all past versions of files without cluttering the file systems with names such as `document_v2.txt`, `document_final.txt`.

Git is also useful for reproducibility: a commit hash uniquely identifies a specific version of a given file.

Git and online platforms such as Github and Gitlab are also very helpful when many people collaborate on the same project. This will be the topic of lab 05.

Note that Git is not the only version-control systems. There are others such as [mercurial](https://www.mercurial-scm.org/). We chose Git because it is currently the most widely used.

## Fetching online data

When possible, it is preferable to use scripts rather than web interfaces to download data files. A script can be self-documenting, can be version-controlled with Git, and can be easily shared with others so that they can reproduce our work. Lab 02 will present reproducible ways to share software.

## Organizing Python code

Python Code that is meant to be reused should be packaged into functions (or classes -- but we will not cover this topic in OpenReproLab) inside modules. These modules can be import from scripts, from notebooks, or even from other modules.

# Other resources

 - [Summary of useful shell commands](https://www.freecodetutorials.com/tutorials/devops/command-line-basics/).
 - [A quick overview of the main Git commands](https://rogerdudler.github.io/git-guide/), for people who already have a basic understanding of Git.
