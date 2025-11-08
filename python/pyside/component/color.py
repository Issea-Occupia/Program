import sys

from qcolor import *
from PySide6.QtWidgets import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        color = Color("red")
        self.setCentralWidget(color)

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec()