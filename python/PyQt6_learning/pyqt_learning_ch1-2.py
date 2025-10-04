from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sys
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.input = QLineEdit()
        self.setCentralWidget(self.input)

        h = self.input.sizeHint().height() + 10
        self.input.setFixedHeight(h)

        pad = 5 
        self.input.setStyleSheet(f"QLineEdit {{ padding-top:{pad}px; padding-bottom:{pad}px; }}")

        self.input.setAlignment(Qt.AlignmentFlag.AlignLeft)
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
