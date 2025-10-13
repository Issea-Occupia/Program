import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QSlider, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("My Window")

        widget = QSlider(Qt.Horizontal)
        widget.setRange(-100, 100)
        widget.setValue(0)
        widget.setSingleStep(1)

        widget.valueChanged.connect(self.value_changed)

        container = QWidget()
        layout =  QHBoxLayout()
        layout.addWidget(widget)
        self.lable = QLabel()
        layout.addWidget(self.lable)
        container.setLayout(layout)
        self.setCentralWidget(container)


    def value_changed(self,i):
        self.lable.setText(str(i))

app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()

