import os
from os import listdir
from PIL import Image
from numpy import asarray

for images in os.listdir("dataset/unProcessed"):
    image = Image.open("dataset/unProcessed/" + images)
    image = image.resize((28, 28))
    image.save("dataset/processed/" + images[:len(images) - 4] + "1.jpg")