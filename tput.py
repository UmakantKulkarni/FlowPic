#!/usr/bin/env python3

import os
import csv
import numpy as np
from argparse import ArgumentParser

company_ports = {
    "webex": [9000, 5004],
    "teams": [3478, 3479, 3480, 3481],
    "zoom": [8801, 8802],
    "google": [19302, 19303, 19304, 19305, 19306, 19307, 19308, 19309, 3478]
}

#common_ports = [80, 443, 3478]
common_ports = []


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


def calc_tput(csv_input_file):
    base_filename = os.path.basename(csv_input_file)
    write_to_file("tput_data.txt", "File-name {}".format(base_filename))
    with open(csv_input_file, 'r') as csv_file:
        j = 1
        port_nums = []        
        reader = csv.reader(csv_file)
        for j, row in enumerate(reader):
            for key in company_ports:
                if base_filename[0:4] == key[0:4]:
                    port_nums = company_ports[key]
            if int(row[2]) in (port_nums + common_ports) or int(
                    row[4]) in (port_nums + common_ports):
                length = int(row[7])
                ts = np.array(row[8:8 + length], dtype=float)
                tot_time = ts[-1]
                if float(tot_time) > 750:
                    sizes = np.array(row[9 + length:-1], dtype=int)
                    ts_diff = np.ediff1d(ts)
                    sz_diff = np.array(sizes[1:], dtype=float)
                    inst_tput_arry = div0(sz_diff, ts_diff)
                    inst_tput = np.nanmax(inst_tput_arry) / (1000 * 1000)
                    sizes_sum = np.sum(sizes)
                    avg_tput = sizes_sum / (tot_time * 1000)
                    tput_dict = {
                        base_filename: {
                            "src_ip": row[1],
                            "dst_ip": row[3],
                            "src_port": row[2],
                            "dst_port": row[4],
                            "total_size": sizes_sum,
                            "total_time": tot_time,
                            "num_packets": length,
                            "init_ts": row[6],
                            "avg_tput": "{} KBPS".format(avg_tput),
                            "inst_tput": "{} MBPS".format(inst_tput)
                        }
                    }
                    print("tput_dict is ", tput_dict)
                    write_to_file("tput_data.txt", tput_dict)
            j = j + 1


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Input CSV file")
    args = parser.parse_args()
    args_dict = vars(args)
    calc_tput(args_dict['file'])