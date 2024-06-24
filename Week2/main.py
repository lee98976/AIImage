from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView
from PySide6.QtGui import QIcon
from scratchWindow import ScratchWindow
import sys

app = QApplication(sys.argv)
app_icon = QIcon("aniconcool.png")
app.setWindowIcon(app_icon)

scene = ScratchWindow(None)
view = QGraphicsView(scene)
view.show()

app.exec()

# from PySide6.QtWidgets import QApplication
# from PySide6.QtGui import QIcon
# from mainWindow import MainWindow
# import sys

# app = QApplication(sys.argv)
# app_icon = QIcon("aniconcool.png")
# app.setWindowIcon(app_icon)

# window = MainWindow(app)
# window.show()
# app.exec()