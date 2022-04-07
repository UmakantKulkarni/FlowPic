#!/usr/bin/env bash

MY_DIR=/home/ukulkarn

for inp_file in $MY_DIR/cs638pcaps/PcapVoip/*.pcap; do
    echo " "
    echo "Working on $inp_file"
    echo " "
    base_name=$(basename -- "$inp_file")
    traffic_type="${base_name%.*}"
    op_csv="$traffic_type.csv"
    python3 $MY_DIR/network-stats/network_stats.py -p $inp_file -e $MY_DIR/FlowPic/csvs/$op_csv
    echo "Generated output CSV file $op_csv"
    echo " "
    python3  $MY_DIR/FlowPic/traffic_csv_converter.py -f $MY_DIR/FlowPic/csvs/$op_csv
    echo "Generated flowpics for $traffic_type"
    echo " "
done