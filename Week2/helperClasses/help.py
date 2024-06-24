from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QPushButton, QStatusBar, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QSlider, QMessageBox, QTextEdit, QScrollArea, QDialogButtonBox, QDialog
from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QAction, QIcon, QFont
from helperClasses.convolutionWidget import ConvolutionWidget
from helperClasses.dense import DenseWidget
from helperClasses.flatten import FlattenWidget
from helperClasses.poolingWidget import PoolingWidget
from helperClasses.trainModel import TrainModel

class HelpDialog(QDialog):
    def __init__(self, type1, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help!")

        self.layout = QVBoxLayout()
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.setCenterButtons(True)
        
        if type1 == "a":
            message1 = QLabel("The filter is the amount of dimensions of the input size for that layer. \n For example, if you have a 20 by 20 picture with three color channels red, green, and blue, then the filter is three.")
        elif type1 == "b":
            message1 = QLabel("The strides is how much the checking in the layer jumps by. \n For example, if strides is two in a one dimensional array, it will check the first two, the second two, and so on.")
        elif type1 == "c":
            message1 = QLabel("Padding only has two options: valid and same. In pooling, each group dictated by strides and group size is combined together. \n The padding of same makes it so that the output size is the same as the input size, while the other doesn't do anything.")
        elif type1 == "d":
            message1 = QLabel("Dimensions describe the size of the array, \n for example a square or 2D array of size 10 has dimensions (10, 10).")
        elif type1 == "e":
            message1 = QLabel("To run your model, simply choose your run type and press run.")
        elif type1 == "f":
            message1 = QLabel("A epoch is a full training runthrough of all the data you provided (Data provided by me).")
        elif type1 == "g":
            message1 = QLabel("Train simply trains your model through the data epoch amount of times.\n Continue training trains your model with any already existing weights. \n Evaluate tests how good your model is against unseen test data. \n Remember, your model can have extremely high accuracy against training data, but is actually bad on generalization on the test data.")
        elif type1 == "h":
            message1 = QLabel("Saving saves your model's layers. \n Loading retreives your model's layers and adds them to any existing layers.")

        self.layout.addWidget(message1)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
    