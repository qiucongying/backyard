import keras
from keras.applications.vgg19 import VGG19
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Input
from keras.models import Model, Sequential
import keras.backend as K
from keras import optimizers
import numpy as np
from keras.preprocessing import image
import pandas as pd
import os
from matplotlib import pyplot as plt
import shutil


def load_labels(file_path):
    assert os.path.isfile(file_path)
    lbl_train = pd.read_csv(file_path)
    return lbl_train

def sort_pictures(df):
    path = '../data/train'
    if os.path.abspath('./')!=path:
        os.chdir(path)
    if len(os.listdir('./')) == 120:
        return
    for breed in pd.unique(df.breed):
        if not os.path.isdir('./'+breed):
            os.mkdir('./'+breed)
    for index in df.index:
        pic_name = df.loc[index,'id'] + '.jpg'
        if os.path.isfile(pic_name):
            bd = df.loc[index,'breed']
            shutil.move(pic_name,bd+'/'+pic_name)
        else:
            print(pic_name)

train_labels = load_labels('./labels.csv')
sort_pictures(train_labels)

img_gen = ImageDataGenerator(rotation_range=2.,
                             zoom_range=0.2,
                             fill_mode='nearest',
                             horizontal_flip=True)


train_generator = img_gen.flow_from_directory('./data/train',
                                              target_size=(224,224),
                                              batch_size=8,
                                              class_mode='categorical',
                                              shuffle=True,
                                             )


my_model = Sequential()
# block 1
my_model.add(Conv2D(filters=64, kernel_size=(3,3), padding='same', input_shape=(224,224,3), name='block1_conv1', activation='relu'))
my_model.add(Conv2D(filters=64, kernel_size=(3,3), padding='same', name='block1_conv2', activation='relu'))
my_model.add(MaxPooling2D(pool_size=(2,2), name='block1_pool'))
# block 2
my_model.add(Conv2D(filters=128, kernel_size=(3,3), padding='same', name='block2_conv1', activation='relu'))
my_model.add(Conv2D(filters=128, kernel_size=(3,3), padding='same', name='block2_conv2', activation='relu'))
my_model.add(MaxPooling2D(pool_size=(2,2), name='block2_pool'))
# block 3
my_model.add(Conv2D(filters=256, kernel_size=(3,3), padding='same', name='block3_conv1', activation='relu'))
my_model.add(Conv2D(filters=256, kernel_size=(3,3), padding='same', name='block3_conv2', activation='relu'))
my_model.add(Conv2D(filters=256, kernel_size=(3,3), padding='same', name='block3_conv3', activation='relu'))
my_model.add(Conv2D(filters=256, kernel_size=(3,3), padding='same', name='block3_conv4', activation='relu'))
my_model.add(MaxPooling2D(pool_size=(2,2), name='block3_pool'))
# block 4
my_model.add(Conv2D(filters=512, kernel_size=(3,3), padding='same', name='block4_conv1', activation='relu'))
my_model.add(Conv2D(filters=512, kernel_size=(3,3), padding='same', name='block4_conv2', activation='relu'))
my_model.add(Conv2D(filters=512, kernel_size=(3,3), padding='same', name='block4_conv3', activation='relu'))
my_model.add(Conv2D(filters=512, kernel_size=(3,3), padding='same', name='block4_conv4', activation='relu'))
my_model.add(MaxPooling2D(pool_size=(2,2), name='block4_pool'))
# block 5
my_model.add(Conv2D(filters=512, kernel_size=(3,3), padding='same', name='block5_conv1', activation='relu'))
my_model.add(Conv2D(filters=512, kernel_size=(3,3), padding='same', name='block5_conv2', activation='relu'))
my_model.add(Conv2D(filters=512, kernel_size=(3,3), padding='same', name='block5_conv3', activation='relu'))
my_model.add(Conv2D(filters=512, kernel_size=(3,3), padding='same', name='block5_conv4', activation='relu'))
my_model.add(MaxPooling2D(pool_size=(2,2), name='block5_pool'))
# fully connect
# my_model.add(Flatten())
# my_model.add(Dense(4096, activation='elu'))
# my_model.add(Dense(120, activation='softmax'))

#os.chdir('../DogBreed')

my_model.load_weights('vgg19_weights_tf_dim_ordering_tf_kernels_notop.h5')

my_model.add(Flatten())
my_model.add(Dense(4096, activation='elu'))
my_model.add(Dense(120, activation='softmax'))

opt = optimizers.Adam()

my_model.compile(loss='categorical_crossentropy',
                    metrics=['categorical_accuracy'],
                    optimizer=opt)

my_model.fit_generator(train_generator, epochs=20, verbose=1)
