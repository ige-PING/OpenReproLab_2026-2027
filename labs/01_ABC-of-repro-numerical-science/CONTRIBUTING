For organizational simplicity, we currently do not accept contributions from people not belonging to OpenReproLab.

For people belonging to OpenReproLab and who wish to contribute, please make sure to always push your changes to both Github and Gitlab.

For that, we recommend setting both remotes as follows:

```sh
git remote add github git@github.com:ige-PING/OpenReproLab_2026-2027.git
git remote add gricad git@gricad-gitlab.univ-grenoble-alpes.fr:ping/openreprolab_2026-2027.git
```

and to use the following convenience shell function when pushing:

```sh
function git-push-current-branch-to-gricad-and-github
{
    local branch=$(git branch | grep -E "^\*" | cut -w -f 2)
    echo "Local branch is \"$branch\""
    for remote in github gricad; do
        if [ $(git remote | grep -cE "^$remote\$") -eq 1 ]; then
            echo "Remote \"$remote\" exists... pushing..."
            git push $remote $branch
        else
            echo "Remote \"$remote\" does not exist!"
        fi
    done
}
```
