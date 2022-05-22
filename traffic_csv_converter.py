#!/usr/bin/env python3
"""
Read traffic_csv
"""

import os
import csv
import random
import numpy as np
from sessions_plotter import *
import glob
from argparse import ArgumentParser

CLASS_LABELS = {"discordaudio": 1, "googleaudio": 2, "skypeaudio": 3, "slackaudio": 4, "teamsaudio": 5, "webexaudio": 6, "zoomaudio": 7, "discordvideo": 8, "googlevideo":9, "skypevideo": 10, "slackvideo": 11, "teamsvideo": 12, "webexvideo": 13, "zoomvideo": 14,  "discordwb": 15, "googlewb":16, "skypewb": 17, "slackwb": 18, "teamswb": 19, "webexwb": 20, "zoomwb": 21, "discordall": 22, "googleall": 23, "skypeall": 24, "slackall": 25, "teamsall": 26, "webexall": 27, "zoomall": 28, "discordvpn": 29, "googlevpn":30, "skypevpn": 31, "slackvpn": 32, "teamsvpn": 33, "webexvpn": 34, "zoomvpn": 35, "disneyreg": 36, "hboreg": 37, "hulureg": 38, "peacockreg": 39, "primereg": 40, "disneyvpn": 41, "hbovpn": 42, "huluvpn": 43, "peacockvpn": 44, "primevpn": 45}
TPS = 60  # TimePerSession in secs
file_save_dir = 'input'
np.random.seed(0)


def traffic_csv_converter(file_path, traffic_type):
    print("Running on " + file_path)
    op_dir = '{}/{}/'.format(image_dir, traffic_type)
    os.makedirs(op_dir, exist_ok=True)
    dataset = []
    # labels = []
    counter = 0
    with open(file_path, 'r') as csv_file:
        if "voip/reg" in file_path:
            DELTA_T = 30
            MIN_TPS = 50
        else:
            DELTA_T = 15
            MIN_TPS = 40
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            if "browsing/reg" in file_path:
                MIN_TPS = 50
                if np.array(row[0]) != "browsing" and np.array(row[0]) != "browsing2-1" and np.array(row[0]) != "SSL_Browsing":
                    continue
            # print row[0], row[7]
            session_tuple_key = tuple(row[:8])
            length = int(row[7])
            ts = np.array(row[8:8+length], dtype=float)
            sizes = np.array(row[9+length:-1], dtype=int)

            # if (sizes > MTU).any():
            #     a = [(sizes[i], i) for i in range(len(sizes)) if (np.array(sizes) > MTU)[i]]
            #     print len(a), session_tuple_key

            if length > 10:
                # print ts[0], ts[-1]
                # h = session_2d_histogram(ts, sizes)
                # session_spectogram(ts, sizes, session_tuple_key[0])
                # dataset.append([h])
                # counter += 1
                # if counter % 100 == 0:
                #     print counter

                for t in range(int(ts[-1]/DELTA_T - TPS/DELTA_T) + 1):
                    mask = ((ts >= t * DELTA_T) & (ts <= (t * DELTA_T + TPS)))
                    # print t * DELTA_T, t * DELTA_T + TPS, ts[-1]
                    ts_mask = ts[mask]
                    sizes_mask = sizes[mask]
                    if len(ts_mask) > 10 and ts_mask[-1] - ts_mask[0] > MIN_TPS:
                        # if "facebook" in session_tuple_key[0]:
                        #     session_spectogram(ts[mask], sizes[mask], session_tuple_key[0])
                        #     # session_2d_histogram(ts[mask], sizes[mask], True)
                        #     session_histogram(sizes[mask], True)
                        #     exit()
                        # else:
                        #     continue

                        h = session_2d_histogram(ts_mask, sizes_mask, traffic_type, plot=True)
                        # session_spectogram(ts_mask, sizes_mask, session_tuple_key[0])
                        dataset.append([h])
                        counter += 1
                        if counter % 100 == 0:
                            print(counter)

    return np.asarray(dataset)  # , np.asarray(labels)


def traffic_class_converter(dir_path):
    dataset_tuple = ()
    for file_path in [os.path.join(dir_path, fn) for fn in next(os.walk(dir_path))[2] if (".csv" in os.path.splitext(fn)[-1])]:
        dataset_tuple += (traffic_csv_converter(file_path),)

    return np.concatenate(dataset_tuple, axis=0)


def export_dataset(csv_file):
    #traffic_type = csv_file.split('.')[0].split('/')[-1]
    #traffic_type = "zoomvideo"
    traffic_type = "disneyreg"
    print("Working on " + csv_file)
    dataset = traffic_csv_converter(csv_file, traffic_type)
    print("Dataset shape is ", dataset.shape)
    #labels = [CLASS_LABELS[traffic_type]]*dataset.shape[0]
    #np.savez(os.path.join(file_save_dir, traffic_type), X=dataset, Y=labels)
    print("Exported " + csv_file)


def random_sampling_dataset(dataset, size=2000, dir_path=""):
    #print("Import dataset " + input_array)
    #dataset = np.load(input_array)
    print(dataset.shape)
    p = size*1.0/len(dataset)
    print(p)
    if p >= 1:
        raise Exception

    mask = np.random.choice([True, False], len(dataset), p=[p, 1-p])
    dataset = dataset[mask]
    print("Start export dataset")

    #np.save(os.path.splitext(input_array)[0] + "_samp", dataset)
    np.save(dir_path.split("/")[2] + "_" + dir_path.split("/")[3], dataset)
    #np.save("browsing_reg_samp", dataset)


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Input CSV file")
    args = parser.parse_args()
    args_dict = vars(args)
    export_dataset(args_dict['file'])