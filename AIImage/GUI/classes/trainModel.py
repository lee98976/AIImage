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
    def __init__(self, preModel):
        self.preModel = preModel # Contains layers information
        #Dataset:
        fashion_mnist = tf.keras.datasets.fashion_mnist
        (self.train_images, self.train_labels), (self.test_images, self.test_labels) = fashion_mnist.load_data()
        self.class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                    'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        #Convert to 0 to 1
        self.train_images = self.train_images / 255.0
        self.test_images = self.test_images / 255.0

        self.firstTimeRun = False
        self.currentThread = "bleh"
    
    # def makeModeFromData(self) -> None:
        
    
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
        self.usePremadeModel()
        self.model.fit(self.train_images, self.train_labels, epochs=15)


    def continueTraining(self) -> None:
        checkpoint_path = "modelWeightSaves/save.weights.h5"
        checkpoint_dir = os.path.dirname(checkpoint_path)

        # Create a callback that saves the model's weights
        cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                        save_weights_only=True,
                                                        verbose=1)
        
        print("Training continued for", 15, "more iterations.")  
        self.model.fit(self.train_images, self.train_labels, epochs=15, callbacks=[cp_callback])

    def evaluatePicture(self, imgName) -> None:
        test_image = Image.open("dataset/processed/" + imgName).convert("L")
        array = asarray(test_image)
        array = (np.expand_dims(array,0))
        array = np.invert(array)
        probability_model = tf.keras.Sequential([self.model, tf.keras.layers.Softmax()])
        predictions_single = probability_model.predict(array)
        print("This picture is a:", self.class_names[np.argmax(predictions_single)])

    def evaluateAccuracy(self, test_images, test_labels, verbose): 
        test_loss, test_acc = self.model.evaluate(test_images, test_labels, verbose=2)
        print(test_acc)

    def menu(self, option, option2):
        def helper(self, option, option2):
            if option == "T":
                self.currentThread = threading.Thread(target=self.trainNew, args=())
                self.currentThread.setDaemon(True)
                self.currentThread.start()
            elif option == "C":
                self.currentThread = threading.Thread(target=self.continueTraining, args=())
                self.currentThread.setDaemon(True)
                self.currentThread.start()
            elif option == "E":
                self.evaluateAccuracy(self.test_images, self.test_labels, 3)
            elif option == "P":
                self.evaluatePicture(option2)
            elif option == "L":
                self.model.load_weights("modelWeightSaves/save.weights.h5")

        if self.firstTimeRun != False:
            if self.currentThread.isAlive():
                return
            helper(self, option, option2)
        else:
            helper(self, option, option2)

def main():
    preModel = []
    trainModelTest = TrainModel(preModel)
    # trainModelTest.menu("T", "")

    while True:
        trainModelTest.menu("T", "")
        print("waiting...")
        time.sleep(2)

main()