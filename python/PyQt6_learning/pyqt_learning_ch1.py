import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("my first window")
        button = QPushButton("push me!!")
        minisize = QSize(300,400)
        maxsize = QSize(600,800)

        self.setCentralWidget(button)
        self.setMinimumSize(minisize)
        self.setMaximumSize(maxsize)

app = QApplication(sys.argv)

window = MainWindows()
window.show()

app.exec()
