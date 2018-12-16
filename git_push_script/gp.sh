#!/bin/bash

# This is a script about wrapping all the tracked changes / changes that has been added
# make a commit, and push into the corresponding origin branch by default.
# This script is create as an automation to bunch of command, like:
#	git commit -am "xxx"
#	git push origin <remote_branch>

RED="\033[0;31m"
GREEN="\033[0;32m"
LIGHTBLUE="\033[0;36m"
ENDC="\033[0m"

PREFIX="[${LIGHTBLUE}$(basename $0)${ENDC}] "
WARN="[${RED}WARN${ENDC}]"
SUCCESS="[${GREEN}SUCCESS${ENDC}]"

echo -e "${PREFIX}Running git_push script..."

GIT=`which git`

# check if the current directory is a git repo
if [ -d .git ]
then
	echo -e "${PREFIX}git repo found! start processing..."
	#echo `${GIT} rev-parse --git-dir 2> /dev/null`
elif [ -z `${GIT} rev-parse --git-dir 2> /dev/null`  ]
then
	echo -e "${PREFIX}${WARN} Cannot find git repo! exiting..."
	exit
fi

# parse args
if [ $# != 1 ]
then
	echo -e "${PREFIX}${WARN} invlaid usage! Using this script with: \n"
	echo "$(basename $0) \"<COMMIT_MESSAGE>\""
	exit
fi 
	
# start checking branches
echo -e "${PREFIX}Start checking commits..." 

BRANCH=`${GIT} branch | grep \* | cut -d ' ' -f 2`
echo -e "${PREFIX}Current branch is ${LIGHTBLUE}${BRANCH}${ENDC}"

# additional checking for master branch
if [ $BRANCH == "master" ]
then
	echo -e "${PREFIX}${WARN} Commiting changes directly into 'master' branch!"
	echo -e "${PREFIX}${WARN} Do you want to continue? y/[N]?"
	read CHOICE
	if [ $CHOICE != 'y' ]
	then
		echo -e "${PREFIX}${WARN} Aborting the pushing. Exit..."
		exit
	fi	
fi

MSG=$1
echo -e "${PREFIX}The commit message is: ${LIGHTBLUE}${MSG}${ENDC}"

# checking the staged files
# if [ -z `${GIT} status | grep 'Changes to be committed:' ` ]

RES=`${GIT} status | grep 'Changes to be committed:' `
if [ -z "${RES}" ]
then
	echo -e "${PREFIX}No files stages... By default adding all the traced file in \
		 to this commit."
	RES=`${GIT} commit -am "${MSG}"`
else
	RES=`${GIT} commit -m "${MSG}"`
fi

if [ -z " `echo ${RES} | grep "\[${BRANCH} [a-f0-9]*\]"` " ]
then
	echo -e "${PREFIX}${WARN} No files included in this commit. Aborting..."
	exit
fi

# push the changes to origin branch
echo -e "${PREFIX}Pushing the changes to origin branch..."
${GIT} push origin ${BRANCH}

echo -e "${PREFIX}Complete."




