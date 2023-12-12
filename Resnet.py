import math
import numpy as np
import scipy
import tensorflow_datasets as tfds
from tensorflow.keras.layers import Input, Add, Dense, Activation, ZeroPadding2D, BatchNormalization, Layer
from tensorflow.keras.layers import Flatten, Conv2D, AveragePooling2D, MaxPooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from mathplotlib.pyplot import imshow
import tensorflow as tf


def ResidualBlock(X, f , filters, stage, block, strides=1):
    # defining name basis
    conv_name_base = 'res' + str(stage) + block + '_branch'
    bn_name_base = 'bn' + str(stage) + block + '_branch'

    # retrieve filters
    F1, F2, F3 = filters

    # save the input value
    X_shortcut = X

    X = Conv2D(filters=F1, kernel_size=(1, 1), strides=(strides, strides), padding='valid', name=conv_name_base + '2a', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2a')(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F2, kernel_size=(f, f), strides=(1, 1), padding='same', name=conv_name_base + '2b', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2b')(X)
    X = Activation('relu')(X)

    X = Conv2D(filters=F3, kernel_size=(1, 1), strides=(1, 1), padding='valid', name=conv_name_base + '2c', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name=bn_name_base + '2c')(X)
    X = Activation('relu')(X)

    if strides != 1:
        X_shortcut = Conv2D(filter=F3, kernel_size=(1, 1), strides=(strides, strides), padding='valid', name=conv_name_base + '1', kernel_initializer=glorot_uniform(seed=0))(X_shortcut)
        X_shortcut = BatchNormalization(axis=3, name=bn_name_base + '1')(X_shortcut)

    X = Add()([X, X_shortcut])
    X = Activation('relu')(X)

    return X

def ResNet50(input_shape, outputClasses):
    # define the input as a tensor with shape input_shape
    X_input = Input(input_shape)

    # zero padding
    X = ZeroPadding2D((3, 3))(X_input)

    # stage 1
    X = Conv2D(64, (7, 7), strides=(2, 2), name='conv1', kernel_initializer=glorot_uniform(seed=0))(X)
    X = BatchNormalization(axis=3, name='bn_conv1')(X)
    X = Activation('relu')(X)
    X = MaxPooling2D((3, 3), strides=(2, 2))(X)

    # stage 2
    X = ResidualBlock(X, f=3, filters=[64, 64, 256], stage=2, block='a', strides=2)
    X = ResidualBlock(X, 3, [64, 64, 256], stage=2, block='b')
    X = ResidualBlock(X, 3, [64, 64, 256], stage=2, block='c')

    # stage 3
    X = ResidualBlock(X, f=3, filters=[128, 128, 512], stage=3, block='a', strides=2)
    X = ResidualBlock(X, 3, [128, 128, 512], stage=3, block='b')
    X = ResidualBlock(X, 3, [128, 128, 512], stage=3, block='c')
    X = ResidualBlock(X, 3, [128, 128, 512], stage=3, block='d')

    # stage 4
    X = ResidualBlock(X, f=3, filters=[256, 256, 1024], stage=4, block='a', strides=2)
    X = ResidualBlock(X, 3, [256, 256, 1024], stage=4, block='b')
    X = ResidualBlock(X, 3, [256, 256, 1024], stage=4, block='c')
    X = ResidualBlock(X, 3, [256, 256, 1024], stage=4, block='d')
    X = ResidualBlock(X, 3, [256, 256, 1024], stage=4, block='e')
    X = ResidualBlock(X, 3, [256, 256, 1024], stage=4, block='f')

    # stage 5
    X = ResidualBlock(X, f=3, filters=[512, 512, 2048], stage=5, block='a', strides=2)
    X = ResidualBlock(X, 3, [512, 512, 2048], stage=5, block='b')
    X = ResidualBlock(X, 3, [512, 512, 2048], stage=5, block='c')

    # avg pool
    X = AveragePooling2D(pool_size=(2, 2), padding='same')(X)

    # output layer
    X = Flatten()(X)
    X = Dense(outputClasses, activation='softmax', name='fc' + str(outputClasses), kernel_initializer=glorot_uniform(seed=0))(X)

    # create model
    model = Model(inputs=X_input, outputs=X, name='ResNet50')

    return model

model = ResNet50(input_shape=(64, 64, 1), outputClasses=10)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()
