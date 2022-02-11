#!/usr/bin/env python3

import os
import numpy as np
from sklearn.model_selection import train_test_split

input_file_dir = 'input'
output_file_dir = 'output'
balanced_dataset = 1
if balanced_dataset:
    input_file_dir = 'input_bal'
    output_file_dir = 'output_bal'
traffic_file_type = 'reg'


if traffic_file_type == 'vpn':
    type1 = 0
else:
    type1 = 1

type2 = 1
type3 = 1
type4 = 1
type5 = 1


def get_train_test_val(x, y):
    X_train_orig, X_test, y_train_orig, y_test = train_test_split(x, y, test_size=0.1, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train_orig, y_train_orig, test_size=0.1, random_state=42)
    return X_train, X_val, X_test, y_train, y_val, y_test


def save_to_file(data_type, d1, d2, d3, d4, d5):
    if type1 == 0:
        np_data = np.concatenate((d2, d3, d4, d5), axis=0)
    else:
        np_data = np.concatenate((d1, d2, d3, d4, d5), axis=0)
    
    np.save(os.path.join(output_file_dir, '{}_{}'.format(traffic_file_type, data_type)), np_data)
    del np_data
    if type1:
        del d1
    del d2
    del d3
    del d4
    del d5


def main():

    if type1:
        a1 = np.load('{}/browsing_{}.npz'.format(input_file_dir, traffic_file_type))
        x1_train, x1_val, x1_test, y1_train, y1_val, y1_test = get_train_test_val(a1['X'], a1['Y'])
        
    if type2:
        a2 = np.load('{}/chat_{}.npz'.format(input_file_dir, traffic_file_type))
        x2_train, x2_val, x2_test, y2_train, y2_val, y2_test = get_train_test_val(a2['X'], a2['Y'])

    if type3:
        a3 = np.load('{}/file_transfer_{}.npz'.format(input_file_dir, traffic_file_type))
        x3_train, x3_val, x3_test, y3_train, y3_val, y3_test = get_train_test_val(a3['X'], a3['Y'])

    if type4:
        a4 = np.load('{}/video_{}.npz'.format(input_file_dir, traffic_file_type))
        x4_train, x4_val, x4_test, y4_train, y4_val, y4_test = get_train_test_val(a4['X'], a4['Y'])

    if type5:
        a5 = np.load('{}/voip_{}.npz'.format(input_file_dir, traffic_file_type))
        x5_train, x5_val, x5_test, y5_train, y5_val, y5_test = get_train_test_val(a5['X'], a5['Y'])

    print("Done splitting")

    if type1 == 0:
        save_to_file('x_train', None, x2_train, x3_train, x4_train, x5_train)
        save_to_file('x_val', None, x2_val, x3_val, x4_val, x5_val)
        save_to_file('x_test', None, x2_test, x3_test, x4_test, x5_test)
        save_to_file('y_train', None, y2_train, y3_train, y4_train, y5_train)
        save_to_file('y_val', None, y2_val, y3_val, y4_val, y5_val)
        save_to_file('y_test', None, y2_test, y3_test, y4_test, y5_test)
    else:
        save_to_file('x_train', x1_train, x2_train, x3_train, x4_train, x5_train)
        save_to_file('x_val', x1_val, x2_val, x3_val, x4_val, x5_val)
        save_to_file('x_test', x1_test, x2_test, x3_test, x4_test, x5_test)
        save_to_file('y_train', y1_train, y2_train, y3_train, y4_train, y5_train)
        save_to_file('y_val', y1_val, y2_val, y3_val, y4_val, y5_val)
        save_to_file('y_test', y1_test, y2_test, y3_test, y4_test, y5_test)

    if type1:
        del a1
    if type2:
        del a2
    if type3:
        del a3
    if type4:
        del a4
    if type5:
        del a5


if __name__ == '__main__':
    main()