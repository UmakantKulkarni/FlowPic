#!/usr/bin/env python3

import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
from pylab import rcParams
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
matplotlib.rcParams.update({'font.size': 16})
#import plotly.graph_objects as go

image_dir = '/Users/umakantkulkarni/Github/FlowPic/images'
MTU = 1500


def session_spectogram_new(ts, sizes, traffic_type, name=None):
    fig = go.Figure(data=go.Scattergl(
    x = ts,
    y = sizes,
    mode='markers',
    marker=dict(
        color="black",
        symbol="square-dot"
    )
))


def session_spectogram(ts, sizes, traffic_type, name=None):
    tsc = list(ts.copy())
    sizesc = list(sizes.copy())
    ck = 0
    pk = 0
    print(len(sizes))
    while ck < len(sizes)-1:
        ck = ck + 1
        if sizes[ck] == sizes[ck-1] and ts[ck] == ts[ck-1]:
            pk = pk + 1
            del sizesc[ck-pk]
            del tsc[ck-pk]
    print("pk", pk)
    ts = tsc.copy()
    sizes = sizesc.copy()
    op_dir = '{}/{}/'.format(image_dir, traffic_type)
    plt.scatter(ts, sizes, marker='s', s=rcParams['lines.markersize'] ** 1, c="0.1")
    plt.ylim(0, MTU+20)
    plt.xlim(0, MTU+20)
    plt.xticks(np.arange(0, MTU+20, 300))
    plt.yticks(np.arange(0, MTU+20, 300))
    #plt.title("{} session spectogram".format(traffic_type))
    plt.ylabel('Size [B]')
    plt.xlabel('Time [sec]')
    #plt.grid(True)
    #plt.show()
    plt.tight_layout()
    plt_name = op_dir + traffic_type + '_' + str(name) + '.pdf'
    plt.savefig(plt_name, bbox_inches='tight')
    plt.close()


def session_histogram(sizes, plot=False):
    hist, bin_edges = np.histogram(sizes, bins=range(0, MTU + 1, 1))
    if plot:
        plt.bar(bin_edges[:-1], hist, width=1)
        plt.xlim(min(bin_edges), max(bin_edges)+100)
        plt.show()
    return hist.astype(np.uint16)


def session_2d_histogram(ts, sizes, traffic_type, plot=False):
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
