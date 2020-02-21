#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Belw is an example of what might be found in this file if your program was written in Python 3.7
# ./input/Border_Crossing_Entry_data.csv ./output/report.csv

workdir=$(pwd)
inputfile="/input/log.csv"
outputfile="/output/report.csv"
concat_path="$workdir$inputfile"
concat_path_out="$workdir$outputfile"
lastLine=$(tail -n 1 "$concat_path")

echo $lastLine

ls

cd src

python3 python3 edgarSessions.py ../input/log.csv ../input/inactivity_period.txt ../output/sessionization.txt
