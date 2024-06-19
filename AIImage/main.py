import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
from tensorflow import keras
from PIL import Image
from numpy import asarray

#How to Start:
#1. CD into AIImage
#2. Run lbozo\Scripts\activate.bat on cmd not powershell
#3. Run main.py

#Dataset:
fashion_mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# print(type(train_images[0]))
# print(train_images[0])

#Convert to 0 to 1
train_images = train_images / 255.0
test_images = test_images / 255.0

#MODEL
model = tf.keras.Sequential()
model.add(tf.keras.layers.Conv2D(2, (2,2), activation='relu', padding="same", input_shape=(28, 28, 1)))
model.summary()
model.add(tf.keras.layers.MaxPool2D(
        pool_size = 2,
        strides = 2,
        padding = "same"
    ))
model.summary()
model.add(tf.keras.layers.Flatten(input_shape=(14, 14)))
model.summary()
model.add(tf.keras.layers.Dense(98, activation='relu'))
model.summary()
model.add(tf.keras.layers.Dense(10))
model.summary()


model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

def useGPU() -> None:
    tf.config.list_physical_devices('GPU')
    print("# of GPUS: ", len(tf.config.list_physical_devices('GPU')))

def modelTrain() -> None:
    checkpoint_path = "Model/save.weights.h5"
    checkpoint_dir = os.path.dirname(checkpoint_path)

    # Create a callback that saves the model's weights
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                    save_weights_only=True,
                                                     verbose=1)
    
    epochs1 = int(input("How many epoches do you want to train? Est: 15 seconds per epoch: "))
    
    if input("Do you want to continue training? Y/N: ") == "N":
        print("Training is not saved. Training for", epochs1, "iterations.")
        model.fit(train_images, train_labels, epochs=epochs1)
    else:
        print("Training continued for", epochs1, "more iterations.")  
        model.fit(train_images, train_labels, epochs=epochs1, callbacks=[cp_callback])

def evaluatePicture(imgName) -> None:
    test_image = Image.open("dataset/processed/" + imgName).convert("L")
    array = asarray(test_image)
    array = (np.expand_dims(array,0))
    array = np.invert(array)
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    predictions_single = probability_model.predict(array)
    print("This picture is a:", class_names[np.argmax(predictions_single)])

def evaluateAccuracy(test_images, test_labels, verbose): 
    test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
    print(test_acc)

while True:
    option = input("What do you want to do? Train, evaluate the accuracy, test it on a picture of your choosing, or load the model with saved weights. T/E/P/L/Exit: ")
    if option == "T":
        modelTrain()
    elif option == "E":
        evaluateAccuracy(test_images, test_labels, 3)
    elif option == "P":
        option2 = input("What is the file name of this picture including the file extension?")
        evaluatePicture(option)
    elif option == "L":
        model.load_weights("Model/save.ckpt")
    elif option == "Exit":
        break

# modelTrain()
# evaluateAccuracy(test_images, test_labels, 3)
# #evaluatePicture("Pullover1.jpg")
