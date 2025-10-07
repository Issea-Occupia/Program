from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        combobox = QComboBox()
        combobox.setEditable(True)
        combobox.setInsertPolicy(QComboBox.InsertPolicy.InsertAlphabetically | QComboBox.InsertPolicy.NoInsert)
        combobox.addItems(['one','two'])
        layout = QHBoxLayout()
        container = QWidget()
        layout.addWidget(combobox)
        container.setLayout(layout)
        combobox.currentIndexChanged.connect(self.index)
        combobox.currentTextChanged.connect(self.text)

        self.setCentralWidget(container)

    def index(self,i):
        print(i)
    
    def text(self,v):
        print(v)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()