from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QPushButton, QStatusBar, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox, QSlider, QMessageBox, QTextEdit, QScrollArea, QDialogButtonBox, QGraphicsView
from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QAction, QIcon, QFont
from helperClasses.convolutionWidget import ConvolutionWidget
from helperClasses.dense import DenseWidget
from helperClasses.flatten import FlattenWidget
from helperClasses.poolingWidget import PoolingWidget
from helperClasses.trainModel import TrainModel
from helperClasses.help import HelpDialog
from helperClasses.saveOrLoad import SaveOrLoad
from scratchWindow import ScratchWindow
import sys
import io
import time

#Commands to run this:
#1. libraries\Scripts\activate.bat; cd GUI; py main.py

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.model = list()

        self.setWindowTitle("AI Model Creator")
        self.createMenuBar()

        # tempF
        # self.fonts = [QFont()]
        self.font = """font-size: 24px;"""

        self.layout = QHBoxLayout()
        self.createUIElements()
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        self.stream = io.StringIO()
        self.old_stdout = sys.stdin
        sys.stdout = self.stream

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateOutput)
        self.modelTrainer = TrainModel(self.model, 0)
        self.timer.start(500)
        

        # lolbutton = QPushButton("lol")
        # lolbutton.clicked.connect(lambda: print(self.model))
        # self.setCentralWidget(lolbutton)

    def createUIElements(self):
        self.inputBox = QVBoxLayout()
        self.outputBox = QVBoxLayout()
        self.modelTextBox = QVBoxLayout()

        self.scratchWindow = ScratchWindow(self)
        self.view = QGraphicsView(self.scratchWindow)
        self.inputBox.addWidget(self.view)
        # # main_widget = QWidget()
        # # layout = QVBoxLayout(main_widget)
        # self.scrollModel = QScrollArea()
        # self.scrollModel.setWidget(self.modelTextBox)
        # self.scrollModel.setWidgetResizable(True)

        self.modelDisplayList = list()

        #Epoches
        epochBox = QHBoxLayout()

        epochLabel = QLabel("Epoches: 0")
        epochLabel.setFixedWidth(70)
        epochBox.addWidget(epochLabel)

        self.epochSlider = QSlider(Qt.Horizontal)
        self.epochSlider.setTickPosition(QSlider.TicksAbove)
        self.epochSlider.setTickInterval(10)
        self.epochSlider.setMinimum(1)
        self.epochSlider.setMaximum(101)
        epochBox.addWidget(self.epochSlider)

        self.epochSlider.valueChanged.connect(lambda: epochLabel.setText("Epoches: " + str(self.epochSlider.value())))

        self.inputBox.addLayout(epochBox)

        dropdownButton = QComboBox()
        dropdownButton.addItems(["Train Model", "Continue Training Model", "Evaluate Model"])
        self.inputBox.addWidget(dropdownButton)

        enterButton = QPushButton("Start")
        enterButton.clicked.connect(lambda: self.startProgram(dropdownButton.currentText()))
        self.inputBox.addWidget(enterButton)

        self.displayModelBox = QHBoxLayout()
        self.displayModelTitle = QLabel("Model")
        self.displayModelTitle.setStyleSheet(self.font)
        self.displayModelTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.displayModelBox.addWidget(self.displayModelTitle)
        self.inputBox.addLayout(self.displayModelBox)

        self.inputBox.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.inputBox.addLayout(self.modelTextBox)
        self.layout.addLayout(self.inputBox)
        #END OF INPUT BOX

        self.titleBox = QHBoxLayout()
        self.outputTitle = QLabel("Output")
        self.outputTitle.setStyleSheet(self.font)
        self.outputTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titleBox.addWidget(self.outputTitle)
        self.outputBox.addLayout(self.titleBox)

        self.outputTerminal = QTextEdit("")
        self.outputText = ""
        self.outputTerminal.setReadOnly(True)
        self.outputBox.addWidget(self.outputTerminal)

        self.layout.addLayout(self.outputBox)

    def createMenuBar(self):
        #Menubar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        save_action = file_menu.addAction("Save")
        saveas_action = file_menu.addAction("Save As")
        load_action = file_menu.addAction("Open Save")
        loadas_action = file_menu.addAction("Open Custom")
        quit_action = file_menu.addAction("Quit")
        save_action.triggered.connect(lambda: self.saveData("temp"))
        saveas_action.triggered.connect(lambda: self.openSaveOrLoad("Save"))
        load_action.triggered.connect(lambda: self.loadData("temp"))
        loadas_action.triggered.connect(lambda: self.openSaveOrLoad("Load"))
        quit_action.triggered.connect(self.quit_app)

        edit_menu = menu_bar.addMenu("Edit")
        
        add_menu = edit_menu.addMenu("Add")

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

        delete_action = edit_menu.addAction("Delete")
        delete_action.triggered.connect(self.modelDelete)

        clear_action = edit_menu.addAction("Clear All")
        clear_action.triggered.connect(self.modelClear)

        help_menu = menu_bar.addMenu("Help")
        layers_button = help_menu.addMenu("Layers")
        filter_button = layers_button.addAction("Filter")
        filter_button.triggered.connect(lambda: self.openHelpWidget("a"))
        strides_button = layers_button.addAction("Strides")
        strides_button.triggered.connect(lambda: self.openHelpWidget("b"))
        padding_button = layers_button.addAction("Padding")
        padding_button.triggered.connect(lambda: self.openHelpWidget("c"))
        dimensions_button = layers_button.addAction("Dimensions")
        dimensions_button.triggered.connect(lambda: self.openHelpWidget("d"))
        run_button = help_menu.addAction("Runnng")
        run_button.triggered.connect(lambda: self.openHelpWidget("e"))
        epoches_button = help_menu.addAction("Epoches")
        epoches_button.triggered.connect(lambda: self.openHelpWidget("f"))
        commands_button = help_menu.addAction("Commands")
        commands_button.triggered.connect(lambda: self.openHelpWidget("g"))
        sal_button = help_menu.addAction("Save + Load")
        sal_button.triggered.connect(lambda: self.openHelpWidget("h"))
        
    def modelDisplayAdd(self):
        # self.modelTextBox.clear()
        # self.modelDisplayList = list()
        # for i in self.model:
        testText = QTextEdit(self.convertModelListToText(self.model[-1]))
        testText.setReadOnly(True)
        self.modelTextBox.addWidget(testText)
        self.modelDisplayList.append(testText)
        self.modelTrainer.buildModel()
        self.outputText = ""
        self.modelTrainer.model.summary()
    
    def modelDelete(self):
        self.modelDisplayList.pop().deleteLater()
        self.model.pop()
    
    def modelClear(self):
        for i in range(len(self.modelDisplayList)):
            self.modelDelete()
        
    def convertModelListToText(self, someList):
        if someList[0] == "pool1D":
            someString = "Pool size: " + str(someList[1]) + ", Strides: " + str(someList[2]) + ", Padding: " + someList[3] + "."
        elif someList[0] == "pool2D":
            someString = "Pool size: (" + str(someList[1][0]) + ", " + str(someList[1][1]) + "), " + "Stride size: (" + str(someList[2][0]) + ", " + str(someList[2][1]) + "), " + "Padding: " + someList[3] + "."
        elif someList[0] == "pool3D":
            someString = "Pool size: (" + str(someList[1][0]) + ", " + str(someList[1][1]) + ", " + str(someList[1][2]) + "), " + "Stride size: (" + str(someList[2][0]) + ", " + str(someList[2][1]) + ", " + str(someList[2][2]) + "), " + "Padding: " + someList[3] + "."
        elif someList[0] == "conv1D":
            someString = "Strides: " + str(someList[1]) + ", Dimensions: (" + str(someList[2][0]) + ", " + str(someList[2][1]) + "), "+ ", Filters: " + str(someList[3]) + ", Padding: " + someList[4] + ", Activation: " + someList[5] + "."
        elif someList[0] == "conv2D":
            someString = "Stride size: (" + str(someList[1][0]) + ", " + str(someList[1][1]) +  "), " + "Dimensions: (" + str(someList[2][0]) + ", " + str(someList[2][1]) + ", " + str(someList[2][2]) + "), " + "Filters: " + str(someList[3]) + ", Padding: " + someList[4] + ", Activation: " + someList[5] + "."
        elif someList[0] == "conv3D":
            someString = "Stride size: (" + str(someList[1][0]) + ", " + str(someList[1][1]) + ", " + str(someList[1][2]) + "), " + "Dimensions: (" + str(someList[2][0]) + ", " + str(someList[2][1]) + ", " + str(someList[2][2]) + ", " + str(someList[2][3]) + "), " + "Filters: " + str(someList[3]) + ", Padding: " + someList[4] + ", Activation: " + someList[5] + "."
        elif someList[0] == "dense":
            someString = "Units: " + str(someList[1]) + ", Activation: " + someList[2] + "."
        elif someList[0] == "flatten":
            someString = "Size of Input: (" + str(someList[1]) + ", " + str(someList[2]) + ")."
        return someString

    def updateOutput(self):
        if len(self.outputText) > 10000 or self.outputTerminal.verticalScrollBar().maximum() > 1000:
            self.outputText = ""
        sys.stdout = self.old_stdout
        temp = repr(self.stream.getvalue())
        if temp == "\n" or temp == "":
            return
        
        self.outputText += self.stream.getvalue()
        self.outputTerminal.setText(self.outputText)
        self.outputTerminal.verticalScrollBar().setValue(self.outputTerminal.verticalScrollBar().maximum())
        self.oldHeight = self.outputTerminal.verticalScrollBar().maximum()
        #self.outputTerminal
        self.stream = io.StringIO()
        self.old_stdout = sys.stdin
        sys.stdout = self.stream

    def saveData(self, fileName):
        self.modelTrainer.checkpoint_path = "modelWeightSaves/" + fileName + ".weights.h5"
        saveFile = open('modelSaves/' + fileName + '.txt', 'w') #Add custom save file names
        saveFile.write(str(len(self.model)))
        saveFile.write("\n")
        for i in self.model:
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
    
    def loadData(self, fileName):
        self.modelTrainer.checkpoint_path = "modelWeightSaves/" + fileName + ".weights.h5"
        fileLoad = open('modelSaves/' + fileName + '.txt', 'r')
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
    
    def startProgram(self, text):
        self.modelTrainer.epoches = self.epochSlider.value()
        if text == "Train Model":
            self.modelTrainer.menu("T", "")
        elif text == "Continue Training Model":
            self.modelTrainer.menu("C", "")
        elif text == "Evaluate Model":
            self.modelTrainer.menu("E", "Pullover1.jpg")
        
    def quit_app(self):
        self.app.quit()
    
    def openHelpWidget(self, type: str):
        widget = HelpDialog(type)
        widget.exec()
    
    def openSaveOrLoad(self, type: str):
        widget = SaveOrLoad(type, self)
        widget.show()
        self.addWindow5 = widget
    
    def openConvolutionWidget(self, type):
        widget = ConvolutionWidget(type, self)
        widget.show()
        self.addWindow1 = widget
    
    def openPoolingWidget(self, type):
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