from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        list = QListWidget()
        list.addItems(['brian','alger','siberian'])

        list.currentItemChanged.connect(self.itemchanged)
        list.currentTextChanged.connect(self.textchanged)

        layout = QVBoxLayout()
        container = QWidget()
        layout.addWidget(list)
        container.setLayout(layout)

        self.setCentralWidget(container)
    def itemchanged(self,i):
        print(i.item())

    def textchanged(self,v):
        print(v)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
