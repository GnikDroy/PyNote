#!/bin/bash

FILENAME=$(basename $1)
FILEPATH=$(dirname $1)
FILE=$(echo $FILENAME | cut -f 1 -d '.')
cd $FILEPATH
gcc -Wall -o "$FILE" *.c  -lm
echo
echo _________________________
echo Press any key to continue
read -n1
