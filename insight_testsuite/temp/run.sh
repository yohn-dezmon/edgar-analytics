#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python
#
#python ./src/sessionization.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt
workdir=$(pwd)
# This is useful to distinguish betweeen test and non-test runs.
parentdir="$(dirname "$(pwd)")"
echo $workdir
echo $parentdir
inputfile="/input/log.csv"
outputfile="/output/sessionization.txt"
concat_path="$workdir$inputfile"
concat_path_out="$workdir$outputfile"
lastLine=$(tail -n 1 "$concat_path")



# cd src
python3 ./src/edgarSessions.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt
