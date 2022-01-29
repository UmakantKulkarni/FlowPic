#!/usr/bin/env python3
import os
import glob
import numpy as np
from sklearn.model_selection import train_test_split

a1 = np.load('input/browsing_reg.npz')
a2 = np.load('input/chat_reg.npz')
a3 = np.load('input/file_transfer_reg.npz')
a4 = np.load('input/video_reg.npz')
a5 = np.load('input/voip_reg.npz')
x1 = a1['X']
x2 = a2['X']
x3 = a3['X']
x4 = a4['X']
x5 = a5['X']
y1 = a1['Y']
y2 = a2['Y']
y3 = a3['Y']
y4 = a4['Y']
y5 = a5['Y']
x = np.concatenate((x1, x2, x3, x4, x5), axis=0)
y = np.concatenate((y1, y2, y3, y4, y5), axis=0)
del a1
del a2
del a3
del a4
del a5
del x1
del x2
del x3
del x4
del x5
del y1
del y2
del y3
del y4
del y5
print("x.shape", x.shape)
print("y.shape", y.shape)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)
print("Done splitting")
del x
del y
np.save(os.path.join('output', 'reg_x_train'), X_train)
del X_train
np.save(os.path.join('output', 'reg_y_train'), y_train)
del y_train
np.save(os.path.join('output', 'reg_x_val'), X_test)
del X_test
np.save(os.path.join('output', 'reg_y_val'), y_test)
del y_test
