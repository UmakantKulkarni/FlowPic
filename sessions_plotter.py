#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
import numpy as np
import time
from pylab import rcParams

image_dir = '/home/ukulkarn/FlowPic/images'
MTU = 1500


def session_spectogram(ts, sizes, traffic_type, name=None):
    op_dir = '{}/{}/'.format(image_dir, traffic_type)
    plt.scatter(ts, sizes, marker='s', s=rcParams['lines.markersize'] ** 1, c="0.1")
    plt.ylim(0, MTU)
    plt.xlim(0, MTU)
    # plt.yticks(np.arange(0, MTU, 10))
    # plt.xticks(np.arange(int(ts[0]), int(ts[-1]), 10))
    plt.title("{} session spectogram".format(traffic_type))
    plt.ylabel('Size [B]')
    plt.xlabel('Time [sec]')
    #plt.grid(True)
    #plt.show()
    plt_name = op_dir + traffic_type + '_' + str(name) + '.png'
    plt.savefig(plt_name)
    plt.close()


def session_histogram(sizes, plot=False):
    hist, bin_edges = np.histogram(sizes, bins=range(0, MTU + 1, 1))
    if plot:
        plt.bar(bin_edges[:-1], hist, width=1)
        plt.xlim(min(bin_edges), max(bin_edges)+100)
        plt.show()
    return hist.astype(np.uint16)


def session_2d_histogram(ts, sizes, traffic_type, plot=True):
    fname = time.time_ns()
    # ts_norm = map(int, ((np.array(ts) - ts[0]) / (ts[-1] - ts[0])) * MTU)
    ts_norm = ((np.array(ts) - ts[0]) / (ts[-1] - ts[0])) * MTU
    H, xedges, yedges = np.histogram2d(sizes, ts_norm, bins=(range(0, MTU + 1, 1), range(0, MTU + 1, 1)))

    if plot:
        session_spectogram(ts_norm, sizes, traffic_type, name=fname)
        if 0:
            plt.pcolormesh(xedges, yedges, H)
            plt.colorbar()
            plt.xlim(0, MTU)
            plt.ylim(0, MTU)
            plt.set_cmap('binary')
            plt.show()
    return H.astype(np.uint16)
