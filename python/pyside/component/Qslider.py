import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QSlider, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox
from PySide6.QtCore import Qt
from random import randint
a = randint(-100, 100)
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My Window")
        self.setwidgets()
        self.setwidget()

    def setwidgets(self):
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(-100)
        self.slider.setMaximum(100)
        self.slider.setSingleStep(1)

        self.label = QLabel(self)
        text = self.slider.value()
        self.label.setText(str(text))

        self.checkbox = QCheckBox(self)
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.changevisibility)
        self.slider.valueChanged.connect(self.setlabletext)

    def setwidget(self):
        layout = QHBoxLayout()
        container = QWidget()
        layout.addWidget(self.label)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.slider)
        container.setLayout(layout)
        self.setCentralWidget(container)

    def changevisibility(self,i):
        self.slider.setVisible(i)

    def setlabletext(self,text):
        self.label.setText(str(text))
app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec()

