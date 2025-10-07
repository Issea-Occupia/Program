from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class Panel(QWidget):
    def __init__(self):
        super().__init__()
        self.input = QLineEdit(self)
        self.label = QLabel("Hello", self)

    def resizeEvent(self, e):
        W, H = self.width(), self.height()
        # 用百分比分配，避免写死像素
        self.input.setGeometry(int(0.05*W), int(0.1*H), int(0.9*W), int(0.2*H))
        self.label.setGeometry(int(0.05*W), int(0.35*H), int(0.9*W), int(0.2*H))
        return super().resizeEvent(e)
 

app = QApplication([])
panel = Panel()  
panel.show() 
app.exec()