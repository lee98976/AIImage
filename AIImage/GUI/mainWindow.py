from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QPushButton, QStatusBar, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSlider, QMessageBox, QTextEdit, QScrollArea
from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QAction, QIcon
from classes.convolutionWidget import ConvolutionWidget
from classes.dense import DenseWidget
from classes.flatten import FlattenWidget
from classes.poolingWidget import PoolingWidget

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.model = list()

        self.setWindowTitle("AI Model Creator")
        self.createMenuBar()

        self.layout = QHBoxLayout()
        self.createUIElements()
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # lolbutton = QPushButton("lol")
        # lolbutton.clicked.connect(lambda: print(self.model))
        # self.setCentralWidget(lolbutton)

    def createUIElements(self):
        self.inputBox = QVBoxLayout()
        self.outputBox = QVBoxLayout()
        self.modelTextBox = QVBoxLayout()

        # # main_widget = QWidget()
        # # layout = QVBoxLayout(main_widget)
        # self.scrollModel = QScrollArea()
        # self.scrollModel.setWidget(self.modelTextBox)
        # self.scrollModel.setWidgetResizable(True)

        self.modelDisplayList = list()

        #Epoches
        epochBox = QHBoxLayout()

        epochLabel = QLabel("0")
        epochBox.addWidget(epochLabel)

        epochSlider = QSlider(Qt.Horizontal)
        epochSlider.setTickPosition(QSlider.TicksAbove)
        epochSlider.setTickInterval(10)
        epochSlider.setMinimum(1)
        epochSlider.setMaximum(99)
        epochBox.addWidget(epochSlider)

        epochSlider.valueChanged.connect(lambda: epochLabel.setText(str(epochSlider.value())))

        self.inputBox.addLayout(epochBox)

        enterButton = QPushButton("Train Model")
        self.inputBox.addWidget(enterButton)

        evaluateButton = QPushButton("Evaluate Model")
        self.inputBox.addWidget(evaluateButton)

        epochSlider2 = QSlider(Qt.Horizontal)
        self.outputBox.addWidget(epochSlider2)

        self.inputBox.addLayout(self.modelTextBox)
        self.layout.addLayout(self.inputBox)
        self.layout.addLayout(self.outputBox)

    def createMenuBar(self):
        #Menubar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        save_action = file_menu.addAction("Save")
        load_action = file_menu.addAction("Load")
        quit_action = file_menu.addAction("Quit")
        save_action.triggered.connect(self.saveData)
        load_action.triggered.connect(self.loadData)
        quit_action.triggered.connect(self.quit_app)

        add_menu = menu_bar.addMenu("Add")

        add_conv = add_menu.addMenu("Convolution Layers")
        add_conv_1d = add_conv.addAction("1D")
        add_conv_1d.triggered.connect(lambda: self.openConvolutionWidget("1D"))
        add_conv_2d = add_conv.addAction("2D")
        add_conv_2d.triggered.connect(lambda: self.openConvolutionWidget("2D"))
        add_conv_3d = add_conv.addAction("3D")
        add_conv_3d.triggered.connect(lambda: self.openConvolutionWidget("3D"))

        add_pool = add_menu.addMenu("Pooling Layer")
        add_pool_1d = add_pool.addAction("1D")
        add_pool_1d.triggered.connect(lambda: self.openPoolingWidget("1D"))
        add_pool_2d = add_pool.addAction("2D")
        add_pool_2d.triggered.connect(lambda: self.openPoolingWidget("2D"))
        add_pool_3d = add_pool.addAction("3D")
        add_pool_3d.triggered.connect(lambda: self.openPoolingWidget("3D"))

        add_flatten = add_menu.addAction("Flatten Layer")
        add_flatten.triggered.connect(self.openFlattenWidget)

        add_dense = add_menu.addAction("Dense Layers")
        add_dense.triggered.connect(self.openDenseWidget)

        add_menu = menu_bar.addMenu("Help")

    def modelDisplayAdd(self):
        # self.modelTextBox.clear()
        # self.modelDisplayList = list()
        # for i in self.model:
        testText = QTextEdit(self.convertModelListToText(self.model[-1]))
        testText.setReadOnly(True)
        self.modelTextBox.addWidget(testText)
        self.modelDisplayList.append(testText)
        
    def convertModelListToText(self, someList):
        if someList[0] == "pool1D":
            someString = "Pool size: " + str(someList[1]) + ", Strides: " + str(someList[2]) + ", Padding: " + someList[3] + "."
        elif someList[0] == "pool2D":
            someString = "Pool size: (" + str(someList[1][0]) + ", " + str(someList[1][1]) + "), " + "Stride size: (" + str(someList[2][0]) + ", " + str(someList[2][1]) + "), " + "Padding: " + someList[3] + "."
        elif someList[0] == "pool3D":
            someString = "Pool size: (" + str(someList[1][0]) + ", " + str(someList[1][1]) + ", " + str(someList[1][2]) + "), " + "Stride size: (" + str(someList[2][0]) + ", " + str(someList[2][1]) + ", " + str(someList[2][2]) + "), " + "Padding: " + someList[3] + "."
        elif someList[0] == "conv1D":
            someString = "Strides: " + str(someList[1]) + ", Padding: " + someList[2] + ", Activation: " + someList[3] + "."
        elif someList[0] == "conv2D":
            someString = "Stride size: (" + str(someList[1][0]) + ", " + str(someList[1][1]) +  "), " + "Padding: " + someList[2] + ", Activation: " + someList[3] + "."
        elif someList[0] == "conv3D":
            someString = "Stride size: (" + str(someList[1][0]) + ", " + str(someList[1][1]) + ", " + str(someList[1][2]) + "), " + "Padding: " + someList[2] + ", Activation: " + someList[3] + "."
        elif someList[0] == "dense":
            someString = "Units: " + str(someList[1]) + ", Activation: " + someList[2] + "."
        elif someList[0] == "flatten":
            someString = "Size of Input: (" + str(someList[1]) + ", " + str(someList[2]) + ")."
        return someString

    def saveData(self):
        saveFile = open('modelSaves/modelSave.txt', 'w')
        saveFile.write(str(len(self.model)))
        saveFile.write("\n")
        for i in self.model: #Add cutsom save file names later
            tempList = list()
            for j in i:
                if isinstance(j, tuple):
                    tempList.append("startOfTuple")
                    for k in j:
                        tempList.append(str(k))
                    tempList.append("endOfTuple")
                else:
                    tempList.append(str(j))
            print(tempList)
            saveFile.write(" ".join(tempList))
            saveFile.write("\n")
        saveFile.close()
    
    def loadData(self):
        fileLoad = open('modelSaves/modelSave.txt', 'r')
        for _ in range(int(fileLoad.readline())):
            tempList = fileLoad.readline().split()
            finalList = list()
            inTuple = False
            currentTuple = list()
            for i in tempList:
                if i == "startOfTuple":
                    inTuple = True
                    currentTuple = list()
                    continue
                elif i == "endOfTuple":
                    inTuple = False
                    finalList.append(tuple(currentTuple))
                    continue
                
                if inTuple == True:
                    currentTuple.append(int(i))
                else:
                    try: finalList.append(int(i))
                    except: finalList.append(i)
            self.model.append(finalList)
            self.modelDisplayAdd()
        fileLoad.close()
        
    def quit_app(self):
        self.app.quit()
    
    def openConvolutionWidget(self, type : str):
        widget = ConvolutionWidget(type, self)
        widget.show()
        self.addWindow1 = widget
    
    def openPoolingWidget(self, type : str):
        widget = PoolingWidget(type, self)
        widget.show()
        self.addWindow2 = widget
    
    def openFlattenWidget(self):
        widget = FlattenWidget(self)
        widget.show()
        self.addWindow3 = widget
    
    def openDenseWidget(self):
        widget = DenseWidget(self)
        widget.show()
        self.addWindow4 = widget
    
    def closeEvent(self, event):
        confirmation = QMessageBox.question(self, "Warning", "Are you sure you want to do this?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes: event.accept()
        else: event.ignore()
#SetGeometry