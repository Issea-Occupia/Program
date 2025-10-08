from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from random import choice
numbers = [0,1,2,3,4,5,6,7,8,9]
alphabet = [chr(i) for i in range(97,123)]

class MainWindows(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")
        self.number = choice(numbers)
        self.letter = choice(alphabet)
        self.button1 = QPushButton(str(self.number))
        self.button2 = QPushButton(self.letter)
        self.button1.pressed.connect(self.number_choice)
        self.button2.pressed.connect(self.letter_choice)
        container = QWidget()
        layout = QVBoxLayout()  
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        container.setLayout(layout)
        self.setCentralWidget(container)
    
    def number_choice(self):
        self.number = choice(numbers)
        self.button1.setText(str(self.number))
        
    def letter_choice(self):
        self.letter = choice(alphabet)
        self.button2.setText(self.letter)
app = QApplication([])

window = MainWindows()
window.show()
app.exec()