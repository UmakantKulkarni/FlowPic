#!/usr/bin/env python3
"""
Read traffic_csv
"""

import os
import csv
from sessions_plotter import *
import glob
from multiprocessing import Process

CLASSES_DIR = "../classes/**/**/"
CLASS_LABELS = {"voip": 0, "video": 1, "file_transfer": 2, "chat": 3, "browsing": 4}

TPS = 60  # TimePerSession in secs
DELTA_T = 15  # Delta T between splitted sessions
MIN_TPS = 40


def traffic_csv_converter(file_path):
    print("Running on " + file_path)
    dataset = []
    # labels = []
    counter = 0
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for i, row in enumerate(reader):
            # print row[0], row[7]
            session_tuple_key = tuple(row[:8])
            length = int(row[7])
            ts = np.array(row[8:8+length], dtype=float)
            sizes = np.array(row[9+length:], dtype=int)

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

                        h = session_2d_histogram(ts_mask, sizes_mask)
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


def export_dataset(class_dir):
    print("Working on " + class_dir)
    dataset = traffic_class_converter(class_dir)
    traffic_ctg = class_dir.split("/")[2]
    traffic_enc = class_dir.split("/")[3]
    file_name = traffic_ctg + "_" + traffic_enc
    labels = [CLASS_LABELS[traffic_ctg]]*dataset.shape[0]
    np.savez(os.path.join('input', file_name), X=dataset, Y=labels)
    print("Exported " + class_dir)


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

    jobs = []
    for class_dir in glob.glob(CLASSES_DIR):
        if "other" not in class_dir:  # "browsing" not in class_dir and
            p = Process(target=export_dataset,
                        args=(class_dir, ))
            jobs.append(p)
            p.start()
    for proc in jobs:
        proc.join()
