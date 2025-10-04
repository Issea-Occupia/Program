from PyQt6.QtWidgets import *
import sys
from random import randint
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.windowTitleChanged.connect(self.titlechanged)
        self.setWindowTitle("Start!!!")
    
    def titlechanged(self,title):
        self.setWindowTitle(str(randint(1,1000000)))
        print(f"changed to {title}")

app = QApplication(sys.argv)
w = MainWindow()
w.show()
app.exec()