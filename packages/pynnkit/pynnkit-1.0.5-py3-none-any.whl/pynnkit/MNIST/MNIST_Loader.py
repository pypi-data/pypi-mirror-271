#
# This is a sample Notebook to demonstrate how to read "MNIST Dataset"
#
import numpy as np # linear algebra
import struct
from array import array
import os
#
# MNIST Data Loader Class
#


class MnistDataloader(object):
    def __init__(self, training_images_filepath,training_labels_filepath,
                 test_images_filepath, test_labels_filepath):
        self.training_images_filepath = training_images_filepath
        self.training_labels_filepath = training_labels_filepath
        self.test_images_filepath = test_images_filepath
        self.test_labels_filepath = test_labels_filepath
    
    def read_images_labels(self, images_filepath, labels_filepath):        
        labels = []
        with open(labels_filepath, 'rb') as file:
            magic, size = struct.unpack(">II", file.read(8))
            if magic != 2049:
                raise ValueError('Magic number mismatch, expected 2049, got {}'.format(magic))
            labels = array("B", file.read())        
        
        with open(images_filepath, 'rb') as file:
            magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
            if magic != 2051:
                raise ValueError('Magic number mismatch, expected 2051, got {}'.format(magic))
            image_data = array("B", file.read())        
        images = []
        for i in range(size):
            images.append([0] * rows * cols)
        for i in range(size):
            img = np.array(image_data[i * rows * cols:(i + 1) * rows * cols])
            img = img.reshape(28, 28)
            images[i][:] = img            
        
        return images, labels
            
    def load_data(self):
        x_train, y_train = self.read_images_labels(self.training_images_filepath, self.training_labels_filepath)
        x_test, y_test = self.read_images_labels(self.test_images_filepath, self.test_labels_filepath)
        return (x_train, y_train),(x_test, y_test)     

#
# Verify Reading Dataset via MnistDataloader class
#

#
# Set file paths based on added MNIST Datasets
#

pref = os.path.dirname(__file__)
training_images_filepath = os.path.join(pref, 'archive', 'train-images-idx3-ubyte', 'train-images-idx3-ubyte')
training_labels_filepath = os.path.join(pref, 'archive', 'train-labels-idx1-ubyte', 'train-labels-idx1-ubyte')
test_images_filepath = os.path.join(pref, 'archive', 't10k-images-idx3-ubyte', 't10k-images-idx3-ubyte')
test_labels_filepath = os.path.join(pref, 'archive', 't10k-labels-idx1-ubyte', 't10k-labels-idx1-ubyte')

#
# Load MINST dataset
#

#loads the original data
def MNIST():

    mnist_dataloader = MnistDataloader(training_images_filepath, training_labels_filepath, test_images_filepath, test_labels_filepath)
    (x_train, y_train), (x_test, y_test) = mnist_dataloader.load_data()

    return (np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test))


#projects the mnist data on a single line of length 28x28 = 784, which is then used to be the size of the input layer.
#returns matrices of shape (784, N) for input or (10, N) for output
#loads with preferred datatype
def MNIST_flat(datatype=np.float64):


    mnist_dataloader = MnistDataloader(training_images_filepath, training_labels_filepath, test_images_filepath, test_labels_filepath)
    (x_train, y_train), (x_test, y_test) = mnist_dataloader.load_data()

    x_train_flat, y_train_flat, x_test_flat, y_test_flat = np.zeros((60000, 784), dtype=datatype), np.zeros((60000, 10), dtype=datatype), np.zeros((10000, 784), dtype=datatype), np.zeros((10000, 10), dtype=datatype)

    last_x = None

    for i in range(len(x_train)):

        
        x_tlist = []
        y_tlist = []

        counter = 0
        for t in range(len(x_train[i])):

            for el in range(len(x_train[i][t])):

                x_train_flat[i][counter] = x_train[i][t][el]
                counter += 1

        #one-hot encoding
        for t in range(10):

            y_train_flat[i][t] = 0

        y_train_flat[i][y_train[i]] = 1



    for i in range(len(x_test)):

        x_tslist = []
        y_tslist = []

        counter = 0
        for t in range(len(x_train[i])):

            for el in range(len(x_train[i][t])):

                x_test_flat[i][counter] = x_test[i][t][el]
                counter += 1

        #one-hot encoding
        for t in range(10):

            y_test_flat[i][t] = 0

        y_test_flat[i][y_test[i]] = 1

    return (x_train_flat.T, y_train_flat.T, x_test_flat.T, y_test_flat.T)

#normalizes the mnist data to [0, 1]
def MNIST_flat_normalized(datatype=np.float32):

    x_train_flat, y_train_flat, x_test_flat, y_test_flat = MNIST_flat(datatype)

    return (x_train_flat/255, y_train_flat/255, x_test_flat/255, y_test_flat/255)
