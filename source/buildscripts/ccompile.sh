#!/usr/bin/env bash

FILENAME=$(basename $1)
FILEPATH=$(dirname $1)
gcc -Wall -c "$1"
echo
echo _________________________
echo Press any key to continue
read -n1
