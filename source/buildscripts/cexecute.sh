#!/usr/bin/env bash

FILENAME=$(basename $1)
FILEPATH=$(dirname $1)
cd $FILEPATH
./$(echo $FILENAME | cut -f 1 -d '.')
echo
echo _________________________
echo Press any key to continue
read -n1
