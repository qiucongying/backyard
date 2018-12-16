# Git Push Script

This is a script that can use the one line command that addes and push changes to corresponding origin branch. It has several feture:

1. Check the current branch name
2. Alert if pushing direct into master branch
3. Commit file checking - if empty commit then do not push


## Sample use

### 0. Befor start
Before use this script, I suggest to download this script to somewhere local, and put an alias to it.
To do so, we can do:

```
git clone https://github.com/qiucongying/backyard.git
cd backyard/git_push_script
echo "alias gp='${PWD}/gp.sh'" >> ~/.bash_profile # add the current gp shell into bash profile
source ~/.bash_profile
```

Then, you are able to use this `gp` script to do the "one line" version of `git commit -am ...` and `git push origin <branch_name>`

## Sample use

```
gp "YOUR_COMMIT_MESSAGE"
```
Yes, just that simple!


## Scenario

### 1 - Auto including all the traced files
Suppose we have bunch of code just changed in our current branch and ready to push to origin. **YOU DIDNT ADD ANY NEW FILE OR `git add`**. The script will include all the traced file into this latest commit and push to origin.

### 2 - Manually added new files
If we have some untracked file in our repo, adding all of them is probably not a good idea, In that case, the script allows the user to add the file they needed manually, instead of adding all file bindly. 

### 3 - Seperate the tracked file into different commit/push
If you only want to add part of the traced file into your latest commmit, you can add them manually with `git add`. Same as #2.2, the script will ignore the files that are not added by the user instead of adding all of them.
