#!/usr/bin/env python3

import os
import numpy as np
from sklearn.model_selection import train_test_split

traffic_file_type = 'reg'
type1 = 1
type2 = 1
type3 = 1
type4 = 1
type5 = 1


def shuffle_data(x, y):
    s = np.arange(x.shape[0])
    np.random.shuffle(s)
    x = x[s]
    y = y[s]
    print(x.shape, y.shape)
    return x, y


def main():

    if type1:
        a1 = np.load('input/browsing_{}.npz'.format(traffic_file_type))
        x1 = a1['X']
        y1 = a1['Y']
    if type2:
        a2 = np.load('input/chat_{}.npz'.format(traffic_file_type))
        x2 = a2['X']
        y2 = a2['Y']
    if type3:
        a3 = np.load('input/file_transfer_{}.npz'.format(traffic_file_type))
        x3 = a3['X']
        y3 = a3['Y']
    if type4:
        a4 = np.load('input/video_{}.npz'.format(traffic_file_type))
        x4 = a4['X']
        y4 = a4['Y']
    if type5:
        a5 = np.load('input/voip_{}.npz'.format(traffic_file_type))
        x5 = a5['X']
        y5 = a5['Y']

    x = np.concatenate((x1, x2, x3, x4, x5), axis=0)
    y = np.concatenate((y1, y2, y3, y4, y5), axis=0)

    if type1:
        del a1
        del x1
        del y1
    if type2:
        del a2
        del x2
        del y2
    if type3:
        del a3
        del x3
        del y3
    if type4:
        del a4
        del x4
        del y4
    if type5:
        del a5
        del x5
        del y5

    print("x.shape", x.shape)
    print("y.shape", y.shape)

    X_train_orig, X_test, y_train_orig, y_test = train_test_split(
        x, y, test_size=0.1, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train_orig,
                                                      y_train_orig,
                                                      test_size=0.1,
                                                      random_state=42)
    X_test, y_test = shuffle_data(X_test, y_test)

    print("Done splitting")
    del x
    del y
    del X_train_orig
    del y_train_orig

    np.save(os.path.join('output', '{}_x_train'.format(traffic_file_type)),
            X_train)
    del X_train
    np.save(os.path.join('output', '{}_y_train'.format(traffic_file_type)),
            y_train)
    del y_train
    np.save(os.path.join('output', '{}_x_test'.format(traffic_file_type)),
            X_test)
    del X_test
    np.save(os.path.join('output', '{}_y_test'.format(traffic_file_type)),
            y_test)
    del y_test
    np.save(os.path.join('output', '{}_x_val'.format(traffic_file_type)),
            X_val)
    del X_val
    np.save(os.path.join('output', '{}_y_val'.format(traffic_file_type)),
            y_val)
    del y_val


if __name__ == '__main__':
    main()