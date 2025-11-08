import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication,QDial,QMainWindow
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setdial()

    def setdial(self):
        self.dial = QDial()
        self.dial.setRange(-100, 90)
        self.dial.setSingleStep(1)
        self.dial.valueChanged.connect(self.value_changed)
        self.dial.sliderMoved.connect(self.position_changed)
        self.setCentralWidget(self.dial)

    def value_changed(self,value):
        print(value)

    def position_changed(self,position):
        print(f"position: {position}")
app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec()