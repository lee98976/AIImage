from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

class DenseWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.layout = QVBoxLayout()
        self.data = data.model
        self.parent = data
        self.helper()
        self.setLayout(self.layout)
    def helper(self):
        horizontalBox = QHBoxLayout()
        unitsLabel = QLabel("Units/Nodes:")
        self.unitsEdit = QLineEdit()
        activationLabel = QLabel("Activation:")
        self.activationEdit = QLineEdit()
        horizontalBox.addWidget(unitsLabel)
        horizontalBox.addWidget(self.unitsEdit)
        horizontalBox.addWidget(activationLabel)
        horizontalBox.addWidget(self.activationEdit)
        self.layout.addLayout(horizontalBox)

        enterButton = QPushButton("Create")
        enterButton.clicked.connect(self.retreiveData)
        self.layout.addWidget(enterButton)
    def retreiveData(self):
        self.data.append(["dense", int(self.unitsEdit.text()), self.activationEdit.text()])
        self.parent.modelDisplayAdd()
        self.close()