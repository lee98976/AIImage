from PySide6.QtWidgets import QApplication, QMainWindow, QToolBar, QPushButton, QStatusBar, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon

class PoolingWidget(QWidget):
    def __init__(self, type, data):
        super().__init__()
        self.layout = QVBoxLayout()
        self.type = type
        self.data = data
        self.helper()
        self.setLayout(self.layout)
    
    def helper(self):
        paddingHorizontalBox = QHBoxLayout()
        paddingLabel = QLabel("Padding (\"valid\" or \"same\"):")
        self.paddingEdit = QLineEdit()
        paddingHorizontalBox.addWidget(paddingLabel)
        paddingHorizontalBox.addWidget(self.paddingEdit)

        # Create Horizontal box to later add to main vbox
        stridesHorizontalBox = QHBoxLayout()
        poolSizeHorizontalBox = QHBoxLayout()

        if self.type == "1D":
            # Create widgets that go inside of Hbox
            stridesLabelX = QLabel("Strides:")
            self.stridesEditX = QLineEdit()
            # Add widgets to the Hbox
            stridesHorizontalBox.addWidget(stridesLabelX)
            stridesHorizontalBox.addWidget(self.stridesEditX)
            # Add Hbox to main Vbox

            poolSizeLabelX = QLabel("Pool Size:")
            self.poolSizeEditX = QLineEdit()
            poolSizeHorizontalBox.addWidget(poolSizeLabelX)
            poolSizeHorizontalBox.addWidget(self.poolSizeEditX)
        elif self.type == "2D":
            stridesLabelX = QLabel("StridesX:")
            self.stridesEditX = QLineEdit()
            stridesLabelY = QLabel("StridesY:")
            self.stridesEditY = QLineEdit()
            stridesHorizontalBox.addWidget(stridesLabelX)
            stridesHorizontalBox.addWidget(self.stridesEditX)
            stridesHorizontalBox.addWidget(stridesLabelY)
            stridesHorizontalBox.addWidget(self.stridesEditY)

            poolSizeLabelX = QLabel("Pool Size X:")
            self.poolSizeEditX = QLineEdit()
            poolSizeLabelY = QLabel("Pool Size Y:")
            self.poolSizeEditY = QLineEdit()
            poolSizeHorizontalBox.addWidget(poolSizeLabelX)
            poolSizeHorizontalBox.addWidget(self.poolSizeEditX)
            poolSizeHorizontalBox.addWidget(poolSizeLabelY)
            poolSizeHorizontalBox.addWidget(self.poolSizeEditY)
        elif self.type == "3D":
            stridesLabelX = QLabel("StridesX:")
            self.stridesEditX = QLineEdit()
            stridesLabelY = QLabel("StridesY:")
            self.stridesEditY = QLineEdit()
            stridesLabelZ = QLabel("StridesZ:")
            self.stridesEditZ = QLineEdit()
            stridesHorizontalBox.addWidget(stridesLabelX)
            stridesHorizontalBox.addWidget(self.stridesEditX)
            stridesHorizontalBox.addWidget(stridesLabelY)
            stridesHorizontalBox.addWidget(self.stridesEditY)
            stridesHorizontalBox.addWidget(stridesLabelZ)
            stridesHorizontalBox.addWidget(self.stridesEditZ)

            poolSizeLabelX = QLabel("Pool Size X:")
            self.poolSizeEditX = QLineEdit()
            poolSizeLabelY = QLabel("Pool Size Y:")
            self.poolSizeEditY = QLineEdit()
            poolSizeLabelZ = QLabel("Pool Size Z:")
            self.poolSizeEditZ = QLineEdit()
            poolSizeHorizontalBox.addWidget(poolSizeLabelX)
            poolSizeHorizontalBox.addWidget(self.poolSizeEditX)
            poolSizeHorizontalBox.addWidget(poolSizeLabelY)
            poolSizeHorizontalBox.addWidget(self.poolSizeEditY)
            poolSizeHorizontalBox.addWidget(poolSizeLabelZ)
            poolSizeHorizontalBox.addWidget(self.poolSizeEditZ)
        
        self.layout.addLayout(stridesHorizontalBox)
        self.layout.addLayout(paddingHorizontalBox)
        self.layout.addLayout(poolSizeHorizontalBox)

        enterButton = QPushButton("Create")
        enterButton.clicked.connect(self.retreiveData)
        self.layout.addWidget(enterButton)
    
    def retreiveData(self):
        if self.type == "1D":
            self.data.append(["pool1D", (self.poolSizeEditX.text()), (self.stridesEditX.text()), self.paddingEdit.text()])
        elif self.type == "2D":
            self.data.append(["pool2D", (self.poolSizeEditX.text(), self.poolSizeEditY.text()), (self.stridesEditX.text(), self.stridesEditY.text()), self.paddingEdit.text()])
        elif self.type == "3D":
            self.data.append(["pool3D", (self.poolSizeEditX.text(), self.poolSizeEditY.text(), self.poolSizeEditZ.text()), (self.stridesEditX.text(), self.stridesEditY.text(), self.stridesEditZ.text()), self.paddingEdit.text()])
        self.close()

class ConvolutionWidget(QWidget):
    def __init__(self, type, data):
        super().__init__()
        self.layout = QVBoxLayout()
        self.type = type
        self.data = data
        self.helper()
        # self.label = QLabel("Add Convolutional Layer")
        # layout.addWidget(self.label)
        self.setLayout(self.layout)

    def helper(self):
        paddingHorizontalBox = QHBoxLayout()
        paddingLabel = QLabel("Padding (\"valid\" or \"same\"):")
        self.paddingEdit = QLineEdit()
        paddingHorizontalBox.addWidget(paddingLabel)
        paddingHorizontalBox.addWidget(self.paddingEdit)

        activationHorizontalBox = QHBoxLayout()
        activationLabel = QLabel("Activation:")
        self.activationEdit = QLineEdit()
        activationHorizontalBox.addWidget(activationLabel)
        activationHorizontalBox.addWidget(self.activationEdit)

        # Create Horizontal box to later add to main vbox
        stridesHorizontalBox = QHBoxLayout()
        if self.type == "1D":
            # Create widgets that go inside of Hbox
            stridesLabelX = QLabel("Strides:")
            self.stridesEditX = QLineEdit()
            # Add widgets to the Hbox
            stridesHorizontalBox.addWidget(stridesLabelX)
            stridesHorizontalBox.addWidget(self.stridesEditX)
            # Add Hbox to main Vbox
        elif self.type == "2D":
            stridesLabelX = QLabel("StridesX:")
            self.stridesEditX = QLineEdit()
            stridesLabelY = QLabel("StridesY:")
            self.stridesEditY = QLineEdit()
            stridesHorizontalBox.addWidget(stridesLabelX)
            stridesHorizontalBox.addWidget(self.stridesEditX)
            stridesHorizontalBox.addWidget(stridesLabelY)
            stridesHorizontalBox.addWidget(self.stridesEditY)
        elif self.type == "3D":
            stridesLabelX = QLabel("StridesX:")
            self.stridesEditX = QLineEdit()
            stridesLabelY = QLabel("StridesY:")
            self.stridesEditY = QLineEdit()
            stridesLabelZ = QLabel("StridesZ:")
            self.stridesEditZ = QLineEdit()
            stridesHorizontalBox.addWidget(stridesLabelX)
            stridesHorizontalBox.addWidget(self.stridesEditX)
            stridesHorizontalBox.addWidget(stridesLabelY)
            stridesHorizontalBox.addWidget(self.stridesEditY)
            stridesHorizontalBox.addWidget(stridesLabelZ)
            stridesHorizontalBox.addWidget(self.stridesEditZ)
        
        self.layout.addLayout(stridesHorizontalBox)
        self.layout.addLayout(paddingHorizontalBox)
        self.layout.addLayout(activationHorizontalBox)

        enterButton = QPushButton("Create")
        enterButton.clicked.connect(self.retreiveData)
        self.layout.addWidget(enterButton)
    
    def retreiveData(self):
        if self.type == "1D":
            self.data.append(["conv1D", (self.stridesEditX.text()), self.paddingEdit.text(), self.activationEdit.text()])
        elif self.type == "2D":
            self.data.append(["conv2D", (self.stridesEditX.text(), self.stridesEditY.text()), self.paddingEdit.text(), self.activationEdit.text()])
        elif self.type == "3D":
            self.data.append(["conv3D", (self.stridesEditX.text(), self.stridesEditY.text(), self.stridesEditZ.text()), self.paddingEdit.text(), self.activationEdit.text()])
        self.close()



class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.model = list()
        self.setWindowTitle("AI Model Creator")

        #Menubar
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        save_action = file_menu.addAction("Save")
        saveAs_action = file_menu.addAction("Save As")
        quit_action = file_menu.addAction("Quit")
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

        add_dense = add_menu.addAction("Dense Layers")

        add_menu = menu_bar.addMenu("Help")

        lolbutton = QPushButton("lol")
        lolbutton.clicked.connect(lambda: print(self.model))
        self.setCentralWidget(lolbutton)
    
    def quit_app(self):
        self.app.quit()
    
    def openConvolutionWidget(self, type : str):
        widget = ConvolutionWidget(type, self.model)
        widget.show()
        self.addWindow1 = widget
    
    def openPoolingWidget(self, type : str):
        widget = PoolingWidget(type, self.model)
        widget.show()
        self.addWindow2 = widget
