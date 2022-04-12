#!/usr/bin/env python3

import os
import csv
import numpy as np


def write_to_file(file_name, file_data):
    with open(file_name, 'a') as the_file:
        the_file.write('\n')
        the_file.write(str(file_data))
        the_file.write('\n')
        the_file.write('\n')


def div0(a, b, fill=np.nan):
    """ a / b, divide by 0 -> `fill`
        div0( [-1, 0, 1], 0, fill=np.nan) -> [nan nan nan]
        div0( 1, 0, fill=np.inf ) -> inf
    """
    with np.errstate(divide='ignore', invalid='ignore'):
        c = np.true_divide(a, b)
    if np.isscalar(c):
        return c if np.isfinite( c ) \
            else fill
    else:
        c[~np.isfinite(c)] = fill
        return c


file_path = "zoom.csv"
j = 1
with open(file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    for j, row in enumerate(reader):
        if int(row[2]) == 8801 or int(row[2]) == 8802 or int(
                row[4]) == 8801 or int(row[4]) == 8802:
            length = int(row[7])
            ts = np.array(row[8:8 + length], dtype=float)
            tot_time = ts[-1]
            if float(tot_time) > 900:
                sizes = np.array(row[9 + length:-1], dtype=int)
                ts_diff = np.ediff1d(ts)
                sz_diff = np.array(sizes[1:], dtype=float)
                inst_tput_arry = div0(sz_diff, ts_diff)  #sz_diff/ts_diff
                inst_tput = np.nanmax(inst_tput_arry) / (1000 * 1000)
                sizes_sum = np.sum(sizes)
                
                tput = sizes_sum / (tot_time * 1000)
                tput_dict = {
                    os.path.basename(file_path): {
                        "src_ip": row[1],
                        "dst_ip": row[3],
                        "src_port": row[2],
                        "dst_port": row[4],
                        "total_size": sizes_sum,
                        "total_time": tot_time,
                        "num_packets": length,
                        "init_ts": row[6],
                        "avg_tput": tput,
                        "inst_tput": inst_tput
                    }
                }
                print("tput_dict is ", tput_dict)
                write_to_file("tput_data.txt", tput_dict)
        j = j + 1
