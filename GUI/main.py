from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from mainWindow import MainWindow
import sys

app = QApplication(sys.argv)
app_icon = QIcon("aniconcool.png")
app.setWindowIcon(app_icon)

window = MainWindow(app)
window.show()
app.exec()