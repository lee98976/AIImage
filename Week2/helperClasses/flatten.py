from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

class FlattenWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.layout = QVBoxLayout()
        self.data = data.model
        self.parent = data
        self.helper()
        self.setLayout(self.layout)
    def helper(self):
        horizontalBox = QHBoxLayout()
        sizeLabelX = QLabel("sizeX:")
        self.sizeEditX = QLineEdit()
        sizeLabelY = QLabel("sizeY:")
        self.sizeEditY = QLineEdit()
        horizontalBox.addWidget(sizeLabelX)
        horizontalBox.addWidget(self.sizeEditX)
        horizontalBox.addWidget(sizeLabelY)
        horizontalBox.addWidget(self.sizeEditY)
        self.layout.addLayout(horizontalBox)

        enterButton = QPushButton("Create")
        enterButton.clicked.connect(self.retreiveData)
        self.layout.addWidget(enterButton)
    def retreiveData(self):
        self.data.append(["flatten", int(self.sizeEditX.text()), int(self.sizeEditY.text())])
        self.parent.modelDisplayAdd()
        self.close()