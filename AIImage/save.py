import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
from tensorflow import keras
from PIL import Image
from numpy import asarray

lbozo = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
lbozo = np.reshape(lbozo, [1, 10, 1])
max_pool_1d = keras.layers.MaxPooling1D(pool_size=5,
   strides=5, padding="valid")

print(max_pool_1d(lbozo))










# model = tf.keras.Sequential([
#     tf.keras.layers.Flatten(input_shape=(28, 28)),
#     tf.keras.layers.Dense(512, activation='relu'),
#     tf.keras.layers.Dense(512, activation='relu'),
#     tf.keras.layers.Dense(10)
# ])

# model.compile(optimizer='adam',
#               loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#               metrics=['accuracy'])