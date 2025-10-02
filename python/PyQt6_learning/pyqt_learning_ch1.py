import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("my first window")
        button = QPushButton("push me!!")
        button.setCheckable(True)
        button.clicked.connect(self.isclicked)
        button.clicked.connect(self.istoggled)
        minisize = QSize(300,400)
        maxsize = QSize(600,800)

        self.setCentralWidget(button)
        self.setMinimumSize(minisize)
        self.setMaximumSize(maxsize)
    def isclicked(self):
        print("the button is clicked!")
    def istoggled(self,checked):
        print("the button is toggled!",checked)
app = QApplication(sys.argv)

window = MainWindows()
window.show()
app.exec()