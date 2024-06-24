from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

class PoolingWidget(QWidget):
    def __init__(self, type, data):
        super().__init__()
        self.layout = QVBoxLayout()
        self.type = type
        self.parent = data
        self.data = data.model
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
            self.data.append(["pool1D", (int(self.poolSizeEditX.text())), (int(self.stridesEditX.text())), self.paddingEdit.text()])
        elif self.type == "2D":
            self.data.append(["pool2D", (int(self.poolSizeEditX.text()), int(self.poolSizeEditY.text())), (int(self.stridesEditX.text()), int(self.stridesEditY.text())), self.paddingEdit.text()])
        elif self.type == "3D":
            self.data.append(["pool3D", (int(self.poolSizeEditX.text()), int(self.poolSizeEditY.text()), int(self.poolSizeEditZ.text())), (int(self.stridesEditX.text()), int(self.stridesEditY.text()), int(self.stridesEditZ.text())), self.paddingEdit.text()])
        self.parent.modelDisplayAdd()
        self.close()