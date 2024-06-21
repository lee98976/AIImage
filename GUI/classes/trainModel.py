import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
from tensorflow import keras
from PIL import Image
from numpy import asarray
import threading
import time
import queue

class TrainModel():
    def __init__(self, preModel, epoches):
        self.preModel = preModel # Contains layers information
        #Dataset:
        fashion_mnist = tf.keras.datasets.fashion_mnist
        (self.train_images, self.train_labels), (self.test_images, self.test_labels) = fashion_mnist.load_data()
        self.class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                    'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        #Convert to 0 to 1
        self.train_images = self.train_images / 255.0
        self.test_images = self.test_images / 255.0
        self.epoches = epoches
        self.currentThread = threading.Thread(target=self.trainNew, args=(), daemon=True)
        self.checkpoint_path = "modelWeightSaves/temp.weights.h5"
    
    # def makeModeFromData(self) -> None:
        
    def buildModel(self) -> None:
        self.model = tf.keras.Sequential()
        for someList in self.preModel:
            if someList[0] == "pool1D":
                self.model.add(tf.keras.layers.MaxPool1D(pool_size=someList[1], strides=someList[2], padding=someList[3]))
            elif someList[0] == "pool2D":
                self.model.add(tf.keras.layers.MaxPool2D(pool_size=(someList[1][0], someList[1][1]), strides=(someList[2][0], someList[2][1]), padding=someList[3]))
            elif someList[0] == "pool3D":
                self.model.add(tf.keras.layers.MaxPool3D(pool_size=(someList[1][0], someList[1][1], someList[1][2]), strides=(someList[2][0], someList[2][1], someList[2][2]), padding=someList[3]))
            elif someList[0] == "conv1D":
                self.model.add(tf.keras.layers.Conv1D(someList[3], someList[3], strides=someList[1], input_shape=(someList[2][0], someList[2][1]), padding=someList[4], activation=someList[5]))
            elif someList[0] == "conv2D":
                self.model.add(tf.keras.layers.Conv2D(someList[3], (someList[3], someList[3]), strides=(someList[1][0], someList[1][1]), input_shape=(someList[2][0], someList[2][1], someList[2][2]), padding=someList[4], activation=someList[5]))
            elif someList[0] == "conv3D":
                self.model.add(tf.keras.layers.Conv3D(someList[3], (someList[3], someList[3], someList[3]), strides=(someList[1][0], someList[1][1], someList[1][2]), input_shape=(someList[2][0], someList[2][1], someList[2][2], someList[2][3]), padding=someList[4], activation=someList[5]))
            elif someList[0] == "dense":
                if someList[2] == "None":
                    self.model.add(tf.keras.layers.Dense(someList[1]))
                else:
                    self.model.add(tf.keras.layers.Dense(someList[1], activation=someList[2]))
            elif someList[0] == "flatten":
                self.model.add(tf.keras.layers.Flatten(input_shape=(someList[1], someList[2])))
            
            self.model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])
    def usePremadeModel(self) -> None:
        #MODEL
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.Conv2D(2, (2,2), activation='relu', padding="same", input_shape=(28, 28, 1)))
        self.model.add(tf.keras.layers.MaxPool2D(
                pool_size = 2,
                strides = 2,
                padding = "same"
            ))
        self.model.add(tf.keras.layers.Flatten(input_shape=(14, 14)))
        self.model.add(tf.keras.layers.Dense(98, activation='relu'))
        self.model.add(tf.keras.layers.Dense(10))

        self.model.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])
        

    def useGPU(self) -> None:
        tf.config.list_physical_devices('GPU')
        print("# of GPUS: ", len(tf.config.list_physical_devices('GPU')))

    def trainNew(self):
        self.buildModel()
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.checkpoint_path,
                                                        save_weights_only=True,
                                                        verbose=1)
        self.model.fit(self.train_images, self.train_labels, epochs=self.epoches, callbacks=[cp_callback], verbose=2)


    def continueTraining(self) -> None:
        # Create a callback that saves the model's weights
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=self.checkpoint_path,
                                                        save_weights_only=True,
                                                        verbose=1)
        
        print("Training continued for", str(self.epoches), "more iterations.")  
        self.buildModel()
        try:
            self.model.load_weights(self.checkpoint_path)
        except:
            pass
        self.model.fit(self.train_images, self.train_labels, epochs=self.epoches, callbacks=[cp_callback], verbose=2)

    def evaluatePicture(self, imgName) -> None:
        self.buildModel()
        self.model.load_weights(self.checkpoint_path)
        test_image = Image.open("dataset/processed/" + imgName).convert("L")
        array = asarray(test_image)
        array = (np.expand_dims(array,0))
        array = np.invert(array)
        probability_model = tf.keras.Sequential([self.model, tf.keras.layers.Softmax()])
        predictions_single = probability_model.predict(array)
        print("This picture is a:", self.class_names[np.argmax(predictions_single)])

    def evaluateAccuracy(self, test_images, test_labels, verbose): 
        self.buildModel()
        self.model.load_weights(self.checkpoint_path)
        test_loss, test_acc = self.model.evaluate(test_images, test_labels, verbose=2)
        print(test_acc)

    def menu(self, option, option2):
        if self.currentThread.is_alive():
            return
        if option == "T":
            self.currentThread = threading.Thread(target=self.trainNew, args=(), daemon=True)
            self.currentThread.start()
        elif option == "C":
            self.currentThread = threading.Thread(target=self.continueTraining, args=(), daemon=True)
            self.currentThread.start()
        elif option == "E":
            self.evaluateAccuracy(self.test_images, self.test_labels, 2)
        elif option == "P":
            self.evaluatePicture(option2)
        elif option == "L":
            self.model.load_weights(self.checkpoint_path)
