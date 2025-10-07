from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App!")
        self.label = QLabel("Hello")
        font = self.label.font()
        font.setPointSize(35)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(self.label)

app = QApplication([])

window = MainWindow()
window.show()

app.exec()