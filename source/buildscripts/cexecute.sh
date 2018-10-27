#!/usr/bin/env bash

./$(echo $1 | cut -f 1 -d '.')
echo
echo _________________________
echo Press any key to continue
read -n1
