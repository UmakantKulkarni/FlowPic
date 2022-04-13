#!/usr/bin/env bash

MY_DIR=/home/ukulkarn

for inp_file in $MY_DIR/FlowPic/csvs/*.csv; do
    if [[ $inp_file == *"zoom"* ]] || [[ $inp_file == *"teams"* ]] || [[ $inp_file == *"webex"* ]] || [[ $inp_file == *"google"* ]]; then
        if [[ $inp_file != *"vpn"* ]]; then
            echo " "
            echo "Working on $inp_file"
            echo " "
            python3 $MY_DIR/FlowPic/tput.py -f $inp_file
            echo " "
            echo "Generated Throughput data for $inp_file"
            echo " "
        fi
    fi
done