#!/usr/bin/env python3

import os
import numpy as np
from sklearn.model_selection import train_test_split

VOIP = ["discord", "slack", "skype", "google", "teams", "webex", "zoom"]
STREAMING = ["disney", "hbo", "hulu", "peacock", "prime"]
VOIP_CATEGORIES = ["audio", "", "wb", "all", "vpn"]
STREAMING_CATEGORIES = ["", "vpn"]
input_file_dir = 'input'

def get_train_test_val(x, y):
    X_train_orig, X_test, y_train_orig, y_test = train_test_split(x, y, test_size=0.1, random_state=42)
    X_train, X_val, y_train, y_val = train_test_split(X_train_orig, y_train_orig, test_size=0.1, random_state=42)
    return X_train, X_val, X_test, y_train, y_val, y_test


def save_voip_to_file(data_type, traffic_file_type, d1, d2, d3, d4, d5, d6, d7):
    if traffic_file_type == "all":
        np_data = np.concatenate((d4, d5, d6, d7), axis=0)
    elif traffic_file_type == "wb":
        np_data = np.concatenate((d1, d3, d4, d5, d6, d7), axis=0)
    else:
        np_data = np.concatenate((d1, d2, d3, d4, d5, d6, d7), axis=0)
    
    if traffic_file_type == "":
        output_file_dir = "output/voip/{}".format("video")
        np.save(os.path.join(output_file_dir, '{}_{}'.format("video", data_type)), np_data)
    else:
        output_file_dir = "output/voip/{}".format(traffic_file_type)
        np.save(os.path.join(output_file_dir, '{}_{}'.format(traffic_file_type, data_type)), np_data)

    del np_data
    if traffic_file_type != "all":
        del d1
    if traffic_file_type != "wb" and traffic_file_type != "all":
        del d2
    if traffic_file_type != "all":
        del d3
    del d4
    del d5
    del d6
    del d7


def save_stream_to_file(data_type, stream_file_type, d1, d2, d3, d4, d5):
    np_data = np.concatenate((d1, d2, d3, d4, d5), axis=0)
    
    if stream_file_type == "":
        output_file_dir = "output/streaming/{}".format("video")
        np.save(os.path.join(output_file_dir, '{}_{}'.format("video", data_type)), np_data)
    else:
        output_file_dir = "output/streaming/{}".format(stream_file_type)
        np.save(os.path.join(output_file_dir, '{}_{}'.format(stream_file_type, data_type)), np_data)

    del np_data
    del d1
    del d2
    del d3
    del d4
    del d5


def main():

    for traffic_file_type in VOIP_CATEGORIES:

        print("Working on traffic_file_type = {}".format(traffic_file_type))

        if traffic_file_type != "all":
            a1 = np.load('{}/{}{}.npz'.format(input_file_dir, VOIP[0], traffic_file_type))
            x1_train, x1_val, x1_test, y1_train, y1_val, y1_test = get_train_test_val(a1['X'], a1['Y'])

        if traffic_file_type != "wb" and traffic_file_type != "all":
            a2 = np.load('{}/{}{}.npz'.format(input_file_dir, VOIP[1], traffic_file_type))
            x2_train, x2_val, x2_test, y2_train, y2_val, y2_test = get_train_test_val(a2['X'], a2['Y'])
        
        if traffic_file_type != "all":
            a3 = np.load('{}/{}{}.npz'.format(input_file_dir, VOIP[2], traffic_file_type))
            x3_train, x3_val, x3_test, y3_train, y3_val, y3_test = get_train_test_val(a3['X'], a3['Y'])

        a4 = np.load('{}/{}{}.npz'.format(input_file_dir, VOIP[3], traffic_file_type))
        x4_train, x4_val, x4_test, y4_train, y4_val, y4_test = get_train_test_val(a4['X'], a4['Y'])

        a5 = np.load('{}/{}{}.npz'.format(input_file_dir, VOIP[4], traffic_file_type))
        x5_train, x5_val, x5_test, y5_train, y5_val, y5_test = get_train_test_val(a5['X'], a5['Y'])

        a6 = np.load('{}/{}{}.npz'.format(input_file_dir, VOIP[5], traffic_file_type))
        x6_train, x6_val, x6_test, y6_train, y6_val, y6_test = get_train_test_val(a6['X'], a6['Y'])

        a7 = np.load('{}/{}{}.npz'.format(input_file_dir, VOIP[6], traffic_file_type))
        x7_train, x7_val, x7_test, y7_train, y7_val, y7_test = get_train_test_val(a7['X'], a7['Y'])

        print("Done VoIP splitting")

        if traffic_file_type == "all":
            save_voip_to_file('x_train', traffic_file_type, None, None, None, x4_train, x5_train, x6_train, x7_train)
            save_voip_to_file('x_val', traffic_file_type, None, None, None, x4_val, x5_val, x6_val, x7_val)
            save_voip_to_file('x_test', traffic_file_type, None, None, None, x4_test, x5_test, x6_test, x7_test)
            save_voip_to_file('y_train', traffic_file_type, None, None, None, y4_train, y5_train, y6_train, y7_train)
            save_voip_to_file('y_val', traffic_file_type, None, None, None, y4_val, y5_val, y6_val, y7_val)
            save_voip_to_file('y_test', traffic_file_type, None, None, None, y4_test, y5_test, y6_test, y7_test)
        elif traffic_file_type == "wb":
            save_voip_to_file('x_train', traffic_file_type, x1_train, None, x3_train, x4_train, x5_train, x6_train, x7_train)
            save_voip_to_file('x_val', traffic_file_type, x1_val, None, x3_val, x4_val, x5_val, x6_val, x7_val)
            save_voip_to_file('x_test', traffic_file_type, x1_test, None, x3_test, x4_test, x5_test, x6_test, x7_test)
            save_voip_to_file('y_train', traffic_file_type, y1_train, None, y3_train, y4_train, y5_train, y6_train, y7_train)
            save_voip_to_file('y_val', traffic_file_type, y1_val, None, y3_val, y4_val, y5_val, y6_val, y7_val)
            save_voip_to_file('y_test', traffic_file_type, y1_test, None, y3_test, y4_test, y5_test, y6_test, y7_test)
        else:
            save_voip_to_file('x_train', traffic_file_type, x1_train, x2_train, x3_train, x4_train, x5_train, x6_train, x7_train)
            save_voip_to_file('x_val', traffic_file_type, x1_val, x2_val, x3_val, x4_val, x5_val, x6_val, x7_val)
            save_voip_to_file('x_test', traffic_file_type, x1_test, x2_test, x3_test, x4_test, x5_test, x6_test, x7_test)
            save_voip_to_file('y_train', traffic_file_type, y1_train, y2_train, y3_train, y4_train, y5_train, y6_train, y7_train)
            save_voip_to_file('y_val', traffic_file_type, y1_val, y2_val, y3_val, y4_val, y5_val, y6_val, y7_val)
            save_voip_to_file('y_test', traffic_file_type, y1_test, y2_test, y3_test, y4_test, y5_test, y6_test, y7_test)

        if traffic_file_type != "all":
            del a1
        if traffic_file_type != "wb" and traffic_file_type != "all":
            del a2
        if traffic_file_type != "all":
            del a3
        del a4
        del a5
        del a6
        del a7
    
    for stream_file_type in STREAMING_CATEGORIES:

        print("Working on stream_file_type = {}".format(stream_file_type))

        b1 = np.load('{}/{}{}.npz'.format(input_file_dir, STREAMING[0], stream_file_type))
        xs1_train, xs1_val, xs1_test, ys1_train, ys1_val, ys1_test = get_train_test_val(b1['X'], b1['Y'])

        b2 = np.load('{}/{}{}.npz'.format(input_file_dir, STREAMING[1], stream_file_type))
        xs2_train, xs2_val, xs2_test, ys2_train, ys2_val, ys2_test = get_train_test_val(b2['X'], b2['Y'])

        b3 = np.load('{}/{}{}.npz'.format(input_file_dir, STREAMING[2], stream_file_type))
        xs3_train, xs3_val, xs3_test, ys3_train, ys3_val, ys3_test = get_train_test_val(b3['X'], b3['Y'])

        b4 = np.load('{}/{}{}.npz'.format(input_file_dir, STREAMING[3], stream_file_type))
        xs4_train, xs4_val, xs4_test, ys4_train, ys4_val, ys4_test = get_train_test_val(b4['X'], b4['Y'])

        b5 = np.load('{}/{}{}.npz'.format(input_file_dir, STREAMING[4], stream_file_type))
        xs5_train, xs5_val, xs5_test, ys5_train, ys5_val, ys5_test = get_train_test_val(b5['X'], b5['Y'])

        print("Done Stream splitting")

        save_stream_to_file('x_train', stream_file_type, xs1_train, xs2_train, xs3_train, xs4_train, xs5_train)
        save_stream_to_file('x_val', stream_file_type, xs1_val, xs2_val, xs3_val, xs4_val, xs5_val)
        save_stream_to_file('x_test', traffic_file_type, xs1_test, xs2_test, xs3_test, xs4_test, xs5_test)
        save_stream_to_file('y_train', traffic_file_type, ys1_train, ys2_train, ys3_train, ys4_train, ys5_train)
        save_stream_to_file('y_val', traffic_file_type, ys1_val, ys2_val, ys3_val, ys4_val, ys5_val)
        save_stream_to_file('y_test', traffic_file_type, ys1_test, ys2_test, ys3_test, ys4_test, ys5_test)



if __name__ == '__main__':
    main()