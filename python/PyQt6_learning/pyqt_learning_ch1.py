from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.thebuttonischecked = True
        self.setWindowTitle("my first window")
        self.button = QPushButton("push me!!")
        self.button.clicked.connect(self.isclicked)
        self.setCentralWidget(self.button)
    def isclicked(self):
        self.button.setText("you already clicked me!")
        self.button.setEnabled(False)
        self.setWindowTitle("my oneshot app")

app = QApplication([])

window = MainWindows()
window.show()
app.exec()