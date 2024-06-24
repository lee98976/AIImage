from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

class ConvolutionWidget(QWidget):
    def __init__(self, type, data):
        super().__init__()
        self.layout = QVBoxLayout()
        self.type = type
        self.data = data.model
        self.parent = data
        self.helper()
        # self.label = QLabel("Add Convolutional Layer")
        # layout.addWidget(self.label)
        self.setLayout(self.layout)

    def helper(self):
        filtersHorizontalBox = QHBoxLayout()
        filtersLabel = QLabel("Filters:")
        self.filtersEdit = QLineEdit()
        filtersHorizontalBox.addWidget(filtersLabel)
        filtersHorizontalBox.addWidget(self.filtersEdit)

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
        dimensionsHorizontalBox = QHBoxLayout()
        if self.type == "1D":
            # Create widgets that go inside of Hbox
            stridesLabelX = QLabel("Strides:")
            self.stridesEditX = QLineEdit()
            # Add widgets to the Hbox
            stridesHorizontalBox.addWidget(stridesLabelX)
            stridesHorizontalBox.addWidget(self.stridesEditX)
            # Add Hbox to main Vbox

            heightLabel = QLabel("Height of Input:")
            self.heightEdit = QLineEdit()
            channelsLabel = QLabel("Channels (3 for RGB, 1 for Grayscale) of Input:")
            self.channelsEdit = QLineEdit()
            dimensionsHorizontalBox.addWidget(heightLabel)
            dimensionsHorizontalBox.addWidget(self.heightEdit)
            dimensionsHorizontalBox.addWidget(channelsLabel)
            dimensionsHorizontalBox.addWidget(self.channelsEdit)
        elif self.type == "2D":
            stridesLabelX = QLabel("StridesX:")
            self.stridesEditX = QLineEdit()
            stridesLabelY = QLabel("StridesY:")
            self.stridesEditY = QLineEdit()
            stridesHorizontalBox.addWidget(stridesLabelX)
            stridesHorizontalBox.addWidget(self.stridesEditX)
            stridesHorizontalBox.addWidget(stridesLabelY)
            stridesHorizontalBox.addWidget(self.stridesEditY)

            heightLabel = QLabel("Height of Input:")
            self.heightEdit = QLineEdit()
            widthLabel = QLabel("Width of Input:")
            self.widthEdit = QLineEdit()
            channelsLabel = QLabel("Channels (3 for RGB, 1 for Grayscale) of Input:")
            self.channelsEdit = QLineEdit()
            dimensionsHorizontalBox.addWidget(heightLabel)
            dimensionsHorizontalBox.addWidget(self.heightEdit)
            dimensionsHorizontalBox.addWidget(widthLabel)
            dimensionsHorizontalBox.addWidget(self.widthEdit)
            dimensionsHorizontalBox.addWidget(channelsLabel)
            dimensionsHorizontalBox.addWidget(self.channelsEdit)
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

            heightLabel = QLabel("Height of Input:")
            self.heightEdit = QLineEdit()
            widthLabel = QLabel("Width of Input:")
            self.widthEdit = QLineEdit()
            breadthLabel = QLabel("Breadth of Input:")
            self.breadthEdit = QLineEdit()
            channelsLabel = QLabel("Channels (3 for RGB, 1 for Grayscale) of Input:")
            self.channelsEdit = QLineEdit()
            dimensionsHorizontalBox.addWidget(heightLabel)
            dimensionsHorizontalBox.addWidget(self.heightEdit)
            dimensionsHorizontalBox.addWidget(widthLabel)
            dimensionsHorizontalBox.addWidget(self.widthEdit)
            dimensionsHorizontalBox.addWidget(breadthLabel)
            dimensionsHorizontalBox.addWidget(self.breadthEdit)
            dimensionsHorizontalBox.addWidget(channelsLabel)
            dimensionsHorizontalBox.addWidget(self.channelsEdit)
        
        self.layout.addLayout(filtersHorizontalBox)
        self.layout.addLayout(stridesHorizontalBox)
        self.layout.addLayout(dimensionsHorizontalBox)
        self.layout.addLayout(paddingHorizontalBox)
        self.layout.addLayout(activationHorizontalBox)

        enterButton = QPushButton("Create")
        enterButton.clicked.connect(self.retreiveData)
        self.layout.addWidget(enterButton)
    
    def retreiveData(self):
        if self.type == "1D":
            self.data.append(["conv1D", (int(self.stridesEditX.text())), 
                              (int(self.heightEdit.text()), int(self.channelsEdit.text())), 
                              int(self.filtersEdit.text()), self.paddingEdit.text(), self.activationEdit.text()])
        elif self.type == "2D":
            self.data.append(["conv2D", (int(self.stridesEditX.text()), int(self.stridesEditY.text())), 
                              (int(self.heightEdit.text()), int(self.widthEdit.text()), int(self.channelsEdit.text())), 
                              int(self.filtersEdit.text()), self.paddingEdit.text(), self.activationEdit.text()])
        elif self.type == "3D":
            self.data.append(["conv3D", (int(self.stridesEditX.text()), int(self.stridesEditY.text()), int(self.stridesEditZ.text())), 
                              (int(self.heightEdit.text()), int(self.widthEdit.text()), int(self.breadthEdit.text()), int(self.channelsEdit.text())), 
                              int(self.filtersEdit.text()), self.paddingEdit.text(), self.activationEdit.text()])
        self.parent.modelDisplayAdd()
        self.close()