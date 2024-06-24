from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

class SaveOrLoad(QWidget):
    def __init__(self, type1, parent):
        super().__init__()
        self.layout = QVBoxLayout()
        self.type = type1
        self.parent = parent
        self.helper()
        self.setLayout(self.layout)
    def helper(self):
        horizontalBox = QHBoxLayout()
        unitsLabel = QLabel("File Name:")
        self.unitsEdit = QLineEdit()
        horizontalBox.addWidget(unitsLabel)
        horizontalBox.addWidget(self.unitsEdit)
        self.layout.addLayout(horizontalBox)

        enterButton = QPushButton("Enter")
        enterButton.clicked.connect(self.finishData)
        self.layout.addWidget(enterButton)
    def finishData(self):
        if self.type == "Save":
            self.parent.saveData(self.unitsEdit.text())
        elif self.type == "Load":
            self.parent.loadData(self.unitsEdit.text())
        self.close()
        