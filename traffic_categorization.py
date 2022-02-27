#!/usr/bin/env python3
# coding: utf-8

# ### Import Libraries

import os
import tensorflow as tf
import numpy as np
import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras import utils
#from keras.layers.normalization import BatchNormalization
from tensorflow.keras.layers import BatchNormalization, Activation, Permute
from tensorflow.keras.callbacks import TensorBoard,ModelCheckpoint
from tensorflow.keras import backend as K
from tensorflow.keras.metrics import top_k_categorical_accuracy


class_names = ["voip", "video", "file_transfer", "chat", "browsing"]
num_classes = len(class_names)
traffic_file_types = ['reg', 'tor', 'vpn']
traffic_file_type = 'merged'
balanced_dataset = 1
input_file_dir = 'output'
MODEL_NAME = "traffic_categorization_{}".format(traffic_file_type)
merged_dataset = 1
if balanced_dataset:
    input_file_dir = 'output_bal'
    MODEL_NAME = "traffic_categorization_{}_bal".format(traffic_file_type)

PATH_PREFIX = "/mydata/flow_pic/FlowPic/{}/".format(input_file_dir)
op_dir = "/mydata/flow_pic/FlowPic/{}_{}/".format(MODEL_NAME, input_file_dir)
log_dir = "/mydata/flow_pic/FlowPic/{}_{}/logs/".format(MODEL_NAME, input_file_dir)
os.makedirs(op_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)


# def set_keras_backend(backend):

#     if K.backend() != backend:
#         os.environ['KERAS_BACKEND'] = backend
#         reload(K)
#         assert K.backend() == backend

# set_keras_backend("theano")
K.set_image_data_format('channels_first')
print(K.backend(), K.image_data_format())

# ### Define Parameters
batch_size = 128
samples_per_epoch = 10
epochs = 40
print_saperator = "###################################################################################################################"

# input hist dimensions
height, width = 1500, 1500
input_shape = (1, height, width)


# ### Import Train and Validation Data

if merged_dataset:

    reg_data = np.load(PATH_PREFIX + "{}_x_train.npy".format(traffic_file_types[0]))
    tor_data = np.load(PATH_PREFIX + "{}_x_train.npy".format(traffic_file_types[1]))
    vpn_data = np.load(PATH_PREFIX + "{}_x_train.npy".format(traffic_file_types[2]))
    x_train = np.concatenate((reg_data, tor_data, vpn_data), axis=0)
    del reg_data
    del tor_data
    del vpn_data

    reg_data = np.load(PATH_PREFIX + "{}_y_train.npy".format(traffic_file_types[0]))
    tor_data = np.load(PATH_PREFIX + "{}_y_train.npy".format(traffic_file_types[1]))
    vpn_data = np.load(PATH_PREFIX + "{}_y_train.npy".format(traffic_file_types[2]))
    y_train_true = np.concatenate((reg_data, tor_data, vpn_data), axis=0)
    del reg_data
    del tor_data
    del vpn_data

    reg_data = np.load(PATH_PREFIX + "{}_x_val.npy".format(traffic_file_types[0]))
    tor_data = np.load(PATH_PREFIX + "{}_x_val.npy".format(traffic_file_types[1]))
    vpn_data = np.load(PATH_PREFIX + "{}_x_val.npy".format(traffic_file_types[2]))
    x_val = np.concatenate((reg_data, tor_data, vpn_data), axis=0)
    del reg_data
    del tor_data
    del vpn_data

    reg_data = np.load(PATH_PREFIX + "{}_y_val.npy".format(traffic_file_types[0]))
    tor_data = np.load(PATH_PREFIX + "{}_y_val.npy".format(traffic_file_types[1]))
    vpn_data = np.load(PATH_PREFIX + "{}_y_val.npy".format(traffic_file_types[2]))
    y_val_true = np.concatenate((reg_data, tor_data, vpn_data), axis=0)
    del reg_data
    del tor_data
    del vpn_data

else:

    x_train = np.load(PATH_PREFIX + "{}_x_train.npy".format(traffic_file_type))
    y_train_true = np.load(PATH_PREFIX + "{}_y_train.npy".format(traffic_file_type))
    x_val = np.load(PATH_PREFIX + "{}_x_val.npy".format(traffic_file_type))
    y_val_true = np.load(PATH_PREFIX + "{}_y_val.npy".format(traffic_file_type))

print(x_train.shape, y_train_true.shape)
print(x_val.shape, y_val_true.shape)


# ### Shuffle Data
np.random.seed(0)
def shuffle_data(x, y):
    s = np.arange(x.shape[0])
    np.random.shuffle(s)
    x = x[s]
    y = y[s]
    print (x.shape, y.shape)
    return x, y

x_train, y_train_true = shuffle_data(x_train, y_train_true)
x_val, y_val_true = shuffle_data(x_val, y_val_true)

print(y_train_true[0:10])


# ### convert class vectors to binary class matrices

y_train = utils.to_categorical(y_train_true, num_classes)
y_val = utils.to_categorical(y_val_true, num_classes)
print(y_train[0:10])
print (y_val[0:10])
print(y_train.shape, y_val.shape)


# ### Define and Compile model

def precision(y_true, y_pred):
    """Precision metric.

    Only computes a batch-wise average of precision.

    Computes the precision, a metric for multi-label classification of
    how many selected items are relevant.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def recall(y_true, y_pred):
    """Recall metric.

    Only computes a batch-wise average of recall.

    Computes the recall, a metric for multi-label classification of
    how many relevant items are selected.
    """
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def f1_score(y_true, y_pred):
    prec = precision(y_true, y_pred)
    rec = recall(y_true, y_pred)
    return 2*((prec*rec)/(prec+rec))

def top_2_categorical_accuracy(y_true, y_pred):
    return top_k_categorical_accuracy(y_true, y_pred, k=2)


#model = Sequential(tf.keras.layers.InputLayer(input_shape=input_shape))
#model.add(Permute((2, 3, 1)))
#model.add(BatchNormalization(axis=-1))
#model.add(Permute((3, 1, 2)))
model = Sequential()
#model.add(BatchNormalization(input_shape=input_shape, axis=-1, momentum=0.99, epsilon=0.001)) ############################
model.add(Conv2D(10, kernel_size=(10, 10),strides=5,padding="same", input_shape=input_shape))
convout1 = Activation('relu')
model.add(convout1)
print(model.output_shape)
model.add(MaxPooling2D(pool_size=(2, 2)))
print(model.output_shape)
model.add(Conv2D(20, (10, 10),strides=5,padding="same"))  #################################################
convout2 = Activation('relu')
model.add(convout2)
print(model.output_shape)
model.add(Dropout(0.25))
model.add(MaxPooling2D(pool_size=(2, 2)))
print(model.output_shape)
model.add(Flatten())
print(model.output_shape)
model.add(Dense(64, activation='relu'))
print(model.output_shape)
model.add(Dropout(0.5))
print(model.output_shape)
model.add(Dense(num_classes, activation='softmax'))
print(model.output_shape)
model.summary()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy', top_2_categorical_accuracy, f1_score, precision, recall])


# ### Define nice_imshow and make_moasic functions

import pylab as pl
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy.ma as ma

def nice_imshow(ax, data, vmin=None, vmax=None, cmap=None, bar=True):
    """Wrapper around pl.imshow"""
    if cmap is None:
        cmap = cm.jet
    if vmin is None:
        vmin = data.min()
    if vmax is None:
        vmax = data.max()
    divider = make_axes_locatable(ax)
    im = ax.imshow(data, vmin=vmin, vmax=vmax, interpolation='nearest', cmap=cmap,origin='lower')
    if bar:
        cax = divider.append_axes("right", size="5%", pad=0.05)
        pl.colorbar(im, cax=cax)

def plotNNFilter2(data, nrows, ncols, layer_name, cmap=None, bar=True):
    """Wrapper around pl.subplot with color bar"""
    if cmap is None:
        cmap = "gray"

    fig, axes = pl.subplots(nrows, ncols,figsize=(5*ncols, 4*nrows))
    for i, ax in enumerate(axes.flat):
        im = ax.imshow(data[:,:,i], interpolation="nearest", cmap=cmap)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        ax.invert_yaxis()

    fig.subplots_adjust(wspace=0.025, hspace=0.05)
    if bar:
        fig.colorbar(im, ax=axes.ravel().tolist())

    pl.savefig(op_dir +  "plotNNFilter2_" + layer_name, bbox_inches='tight', pad_inches=1)
    #pl.show()
    pl.close()

def plotNNFilter(data, nrows, ncols, layer_name, cmap=None, bar=True):
    """Wrapper around pl.subplot"""
    if cmap is None:
        cmap = "gray"

    pl.figure(figsize=(3*ncols, 3*nrows))

    for i in range(nrows*ncols):
        pl.subplot(nrows, ncols, i+1)
        pl.imshow(data[:,:,i], interpolation="nearest", cmap=cmap)
        pl.xticks([])
        pl.yticks([])
        pl.gca().invert_yaxis()
    pl.subplots_adjust(wspace=0.025, hspace=0.05)
    pl.savefig(op_dir +  "plotNNFilter_" + layer_name, bbox_inches='tight', pad_inches=1)
    #pl.show()
    pl.close()

def make_mosaic(imgs, nrows, ncols, border=1):
    """
    Given a set of images with all the same shape, makes a
    mosaic with nrows and ncols
    """
    nimgs = imgs.shape[2]
    imshape = imgs.shape[0:2]

    mosaic = ma.masked_all((nrows * imshape[0] + (nrows - 1) * border,
                            ncols * imshape[1] + (ncols - 1) * border),
                            dtype=np.float32)

    paddedh = imshape[0] + border
    paddedw = imshape[1] + border
    for i in range(nimgs):
        row = int(np.floor(i / ncols))
        col = i % ncols

        mosaic[row * paddedh:row * paddedh + imshape[0],
               col * paddedw:col * paddedw + imshape[1]] = imgs[:,:,i]
    return mosaic

def mosaic_imshow(imgs, nrows, ncols, cmap=None, border=1, layer_name="convout"):
    pl.figure(figsize=(3*ncols, 3*nrows))
    #     pl.suptitle('convout2')
    nice_imshow(pl.gca(), make_mosaic(imgs, nrows, ncols, border=border), cmap=cmap)
    pl.savefig(op_dir +  "mosaic_imshow_" + layer_name, bbox_inches='tight', pad_inches=1)
    #pl.show()
    pl.close()

# pl.imshow(make_mosaic(np.random.random((10, 10, 9)), 3, 3, border=1))
# pl.show()


# Visualize the first layer of convolutions on an input image
i = 35
X = x_train[i][0]
print(X)
print(y_train_true[i])
pl.figure(figsize=(15, 15))
pl.title('input')
nice_imshow(pl.gca(), np.squeeze(X), vmin=0, vmax=1, cmap=cm.binary)
pl.savefig(op_dir +  "input", bbox_inches='tight', pad_inches=1)
#pl.show()
pl.close()

# Visualize convolution result (after activation)
def get_layer_output(layer, input_img, layer_name):
    convout_f = K.function(model.inputs, [layer.output])
    C = convout_f([input_img])
    C = np.squeeze(C)
    print(layer_name + " output shape : ", C.shape)
    C = np.transpose(C)
    C = np.swapaxes(C,0,1)
    print(layer_name + " output shape : ", C.shape)
    return C


if 1:
    C1 = get_layer_output(convout1, x_train[i:i+1], layer_name="convout1_before")
    mosaic_imshow(C1, 2, 5, cmap=cm.binary, border=2, layer_name="convout1_before")
    plotNNFilter(C1, 2, 5, cmap=cm.binary, layer_name="convout1_before")
    plotNNFilter2(C1, 2, 5, cmap=cm.binary, layer_name="convout1_before")

    C2 = get_layer_output(convout2, x_train[i:i+1], layer_name="convout2_before")
    mosaic_imshow(C2, 4, 5, cmap=cm.binary, border=2, layer_name="convout2_before")
    plotNNFilter(C2, 4, 5, cmap=cm.binary, layer_name="convout2_before")
    plotNNFilter2(C2, 4, 5, cmap=cm.binary, layer_name="convout2_before")


    # Visualize weights
    W1 = model.layers[0].get_weights()[0]
    W1 = np.squeeze(W1)
    # W1 = np.asarray(W1)
    print("W1 shape : ", W1.shape)

    mosaic_imshow(W1, 2, 5, cmap=cm.binary, border=1, layer_name="conv1_weights_before")
    plotNNFilter(W1, 2, 5, cmap=cm.binary, layer_name="conv1_weights_before")
    plotNNFilter2(W1, 2, 5, cmap=cm.binary, layer_name="conv1_weights_before")

    # Visualize weights
    W2 = model.layers[3].get_weights()[0][:,:,0,:]
    W2 = np.asarray(W2)
    print("W2 shape : ", W2.shape)

    mosaic_imshow(W2, 4, 5, cmap=cm.binary, border=1, layer_name="conv2_weights_before")
    plotNNFilter(W2, 4, 5, cmap=cm.binary, layer_name="conv2_weights_before")
    plotNNFilter2(W2, 4, 5, cmap=cm.binary, layer_name="conv2_weights_before")


# ### Fit model on training data

tensorboard = TensorBoard(log_dir=log_dir, histogram_freq=1, write_grads=True, write_graph=True,
                          write_images=True, batch_size=batch_size)
checkpointer_loss = ModelCheckpoint(filepath= op_dir + 'loss.hdf5', verbose=1, save_best_only=True, save_weights_only=True)
checkpointer_acc = ModelCheckpoint(monitor='val_acc', filepath= op_dir + 'acc.hdf5', verbose=1, save_best_only=True, save_weights_only=True)
tensorboard.set_model(model)

def generator(features, labels, batch_size):
    index = 0
    while True:
        index += batch_size
        if index >= len(features):
            batch_features = np.append(features[index-batch_size:len(features)], features[0:index-len(features)], axis=0)
            batch_labels = np.append(labels[index-batch_size:len(features)], labels[0:index-len(features)], axis=0)
            index -= len(features)
            yield batch_features, batch_labels
        else:
            yield features[index-batch_size:index], labels[index-batch_size:index]

history = model.fit_generator(generator(x_train, y_train, batch_size),
          epochs=epochs,
          steps_per_epoch=samples_per_epoch,
          verbose=2,
          callbacks=[tensorboard,checkpointer_loss,checkpointer_acc],
          validation_data=(x_val, y_val))


# ### Plot history accuracy

import matplotlib.pyplot as plt
import pickle

with open(op_dir +  "accuracy.pkl", 'wb') as output:
    pickle.dump(history.history, output, pickle.HIGHEST_PROTOCOL)

# list all data in history
print(history.history.keys())
x = np.asarray(range(1,epochs + 1))
# summarize history for accuracy
plt.figure()
plt.plot(x, history.history['accuracy'])
plt.plot(x, history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'val'], loc='upper left')
plt.savefig(op_dir +  "accuracy_history", bbox_inches='tight', pad_inches=1)
#plt.show()
plt.close()


# ### Plot Confusion Matrix

y_val_prediction = model.predict_classes(x_val, verbose=1)


print(y_val_prediction[:10])



from sklearn.metrics import confusion_matrix
import itertools

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          fname='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.1f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, format(cm[i, j]*100, fmt) + '%',
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(fname, bbox_inches='tight', pad_inches=1)
    plt.close()

# Compute confusion matrix
cnf_matrix = confusion_matrix(y_val_true, y_val_prediction)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names,
                      title='Confusion matrix, without normalization',
                      fname=op_dir + 'Confusion_matrix_without_normalization')

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title='Normalized confusion matrix',
                      fname=op_dir + 'Normalized_confusion_matrix')

#plt.show()


def stats(y_true, y_pred):
    correct = sum([1 for i,pred in enumerate(y_pred) if y_true[i][pred]==1])
    print(y_true.shape[0], correct, correct*1.0/len(y_true))

    for class_ind in range(y_true.shape[1]):
        total_ind = len([1 for val in y_true if val[class_ind]==1])
        correct_ind = sum([1 for i,pred in enumerate(y_pred) if (pred == class_ind and y_true[i][pred]==1)])
        print(class_ind, total_ind, correct_ind, correct_ind*1.0/total_ind)

stats(y_val, y_val_prediction)
# stats(y_test_vpn, y_test_vpn_prediction)
# stats(y_test_tor, y_test_tor_prediction)
# correct_1 = sum([1 for i,pred in enumerate(y_test_prediction) if (pred == 1 and y_test[i][pred]==1)])
# print correct_1, correct_1*1.0/len([1 for val in y_test if val[1]==1])


from sklearn.metrics import classification_report
print(classification_report(y_val_true, y_val_prediction))


# Visualize the first layer of convolutions on an input image
X = x_train[i][0]
print(X)
print(y_train_true[i])
pl.figure(figsize=(15, 15))
nice_imshow(pl.gca(), np.squeeze(X), vmin=0, vmax=1, cmap=cm.binary)
pl.savefig(op_dir +  "input_" + str(int(y_train_true[i])), bbox_inches='tight', pad_inches=1)
#pl.show()
pl.close()

# Visualize convolution result (after activation)
def get_layer_output(layer, input_img, layer_name):
    convout_f = K.function(model.inputs, [layer.output])
    C = convout_f([input_img])
    C = np.squeeze(C)
    print(layer_name + " output shape : ", C.shape)
    C = np.transpose(C)
    C = np.swapaxes(C,0,1)
    print(layer_name + " output shape : ", C.shape)
    return C


C1 = get_layer_output(convout1, x_train[i:i+1], layer_name="convout1_" + str(int(y_train_true[i])))
mosaic_imshow(C1, 2, 5, cmap=cm.binary, border=2, layer_name="convout1_" + str(int(y_train_true[i])))
plotNNFilter(C1, 2, 5, cmap=cm.binary, layer_name="convout1_" + str(int(y_train_true[i])))
plotNNFilter2(C1, 2, 5, cmap=cm.binary, layer_name="convout1_" + str(int(y_train_true[i])))

C2 = get_layer_output(convout2, x_train[i:i+1], layer_name="convout2_" + str(int(y_train_true[i])))
mosaic_imshow(C2, 4, 5, cmap=cm.binary, border=2, layer_name="convout2_" + str(int(y_train_true[i])))
plotNNFilter(C2, 4, 5, cmap=cm.binary, layer_name="convout2_" + str(int(y_train_true[i])))
plotNNFilter2(C2, 4, 5, cmap=cm.binary, layer_name="convout2_" + str(int(y_train_true[i])))

# Visualize weights
W1 = model.layers[0].get_weights()[0]
W1 = np.squeeze(W1)
# W1 = np.asarray(W1)
print("W1 shape : ", W1.shape)

mosaic_imshow(W1, 2, 5, cmap=cm.binary, border=1, layer_name="conv1_weights")
plotNNFilter(W1, 2, 5, cmap=cm.binary, layer_name="conv1_weights")
plotNNFilter2(W1, 2, 5, cmap=cm.binary, layer_name="conv1_weights")

# Visualize weights
W2 = model.layers[3].get_weights()[0][:,:,0,:]
W2 = np.asarray(W2)
print("W2 shape : ", W2.shape)

mosaic_imshow(W2, 4, 5, cmap=cm.binary, border=1, layer_name="conv2_weights")
plotNNFilter(W2, 4, 5, cmap=cm.binary, layer_name="conv2_weights")
plotNNFilter2(W2, 4, 5, cmap=cm.binary, layer_name="conv2_weights")


y_val_true, y_val_prediction

for j in range(len(y_val_true)):
    if y_val_true[j] == 0 and y_val_prediction[j] == 1:
        print(j, sum(sum(sum(x_val[j]))))
#         pl.figure(figsize=(10, 10))
#         pl.title('input ' + str(j))
#         nice_imshow(pl.gca(), np.squeeze(x_val[j]), vmin=0, vmax=1, cmap=cm.binary)
#         pl.savefig(op_dir +  "input", bbox_inches='tight', pad_inches=1)
#         pl.show()
#         pl.close()

print(print_saperator)

score_val = model.evaluate(x_val, y_val, verbose=1)
print('Validation loss:', score_val[0])
print('Validaion accuracy:', score_val[1])
print('Validaion top_2_categorical_accuracy:', score_val[2])

cnf_matrix_val = confusion_matrix(y_val_true, y_val_prediction)

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix_val, classes=class_names, normalize=True,
                      title='Normalized confusion matrix for validation set',
                      fname=op_dir + "val_" + 'Normalized_confusion_matrix')


print(print_saperator)
# Evaluate model on test data

if merged_dataset:
    
    reg_data = np.load(PATH_PREFIX + "{}_x_test.npy".format(traffic_file_types[0]))
    tor_data = np.load(PATH_PREFIX + "{}_x_test.npy".format(traffic_file_types[1]))
    vpn_data = np.load(PATH_PREFIX + "{}_x_test.npy".format(traffic_file_types[2]))
    x_test = np.concatenate((reg_data, tor_data, vpn_data), axis=0)
    del reg_data
    del tor_data
    del vpn_data

    reg_data = np.load(PATH_PREFIX + "{}_y_test.npy".format(traffic_file_types[0]))
    tor_data = np.load(PATH_PREFIX + "{}_y_test.npy".format(traffic_file_types[1]))
    vpn_data = np.load(PATH_PREFIX + "{}_y_test.npy".format(traffic_file_types[2]))
    y_test_true = np.concatenate((reg_data, tor_data, vpn_data), axis=0)
    del reg_data
    del tor_data
    del vpn_data

else:

    x_test = np.load(PATH_PREFIX + "{}_x_test.npy".format(traffic_file_type))
    y_test_true = np.load(PATH_PREFIX + "{}_y_test.npy".format(traffic_file_type))

x_test, y_test_true = shuffle_data(x_test, y_test_true)
y_test = utils.to_categorical(y_test_true, num_classes)

score = model.evaluate(x_test, y_test, verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
print('Test top_2_categorical_accuracy:', score[2])

y_test_prediction = model.predict_classes(x_test, verbose=1)
cnf_matrix = confusion_matrix(y_test_true, y_test_prediction)

print(x_test.shape, y_test.shape)

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                    title='Normalized confusion matrix for test set',
                    fname=op_dir + "test_" + 'Normalized_confusion_matrix')



# ### Save Model and weights

model_json = model.to_json()
with open(op_dir + MODEL_NAME + '.json', "w") as json_file:
    json_file.write(model_json)
model.save_weights(op_dir + MODEL_NAME + '.h5')
print("Save Model")