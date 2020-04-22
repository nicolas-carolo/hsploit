#!/bin/bash
HOUNDSPLOIT_PATH="/User/$USER/HoundSploit"

if [ $(id -u) = 0 ]; then
	echo "ERROR: This script must NOT be run as 'root'"
	exit 1
fi

if ! [ $(uname) == "Darwin" ] ; then
    echo "ERROR: This installation script is only for systems running macOS"
    exit 1
fi

if ! [ -d "$HOUNDSPLOIT_PATH" ] ; then
    mkdir $HOUNDSPLOIT_PATH
fi

if ! [ -d "$HOUNDSPLOIT_PATH/exploitdb" ] ; then
    cd $HOUNDSPLOIT_PATH
    git clone https://github.com/offensive-security/exploitdb
else
    cd $HOUNDSPLOIT_PATH/exploitdb
    git_output=$(git pull)
	if [ "$git_output" == "Already up to date." ]  ; then
        echo "Database already up-to-date"
    else
        if [ -f "$HOUNDSPLOIT_PATH/hound_db.sqlite3" ] ; then
            rm $HOUNDSPLOIT_PATH/hound_db.sqlite3
        fi
        echo "Latest version of the database downloaded"
    fi
fi

if ! [ -d "$HOUNDSPLOIT_PATH/hsploit" ] ; then
    git clone https://github.com/nicolas-carolo/hsploit $HOUNDSPLOIT_PATH/hsploit
fi

cd $HOUNDSPLOIT_PATH/hsploit
git_output=$(git pull)
if [ "$git_output" == "Already up to date." ]  ; then
    echo "hsploit already up-to-date"
else
    echo "Latest version of hsploit downloaded"
    echo "Run the following commands (be sure to use the Python 3 interpreter)"
    echo -e "\t$ pip install -r $HOUNDSPLOIT_PATH/hsploit/requirements.txt"
    echo -e "\t$ cd $HOUNDSPLOIT_PATH/hsploit"
    echo -e "\t$ python setup.py install"
    echo -e "\t$ hsploit"
fi