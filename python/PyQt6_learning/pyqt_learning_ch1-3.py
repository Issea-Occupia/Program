from PyQt6.QtWidgets import *
from PyQt6.QtCore import * 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        container = QWidget()

        self.checkbox = QCheckBox()
        self.combobox = QComboBox()
        self.dateedit = QDateEdit()
        self.datetimeedit = QDateTimeEdit()
        self.dial = QDial()
        self.doublespinbox = QDoubleSpinBox()
        self.fontcombobox = QFontComboBox()
        self.lcdnumber = QLCDNumber()
        self.processbar = QProgressBar()
        self.radiobutton = QRadioButton()
        self.slider = QSlider()
        self.spinbox = QSpinBox()
        self.timeedit = QTimeEdit()
        layout.addWidget(self.checkbox)
        layout.addWidget(self.combobox)
        layout.addWidget(self.dateedit)
        layout.addWidget(self.datetimeedit)
        layout.addWidget(self.dial)
        layout.addWidget(self.doublespinbox)
        layout.addWidget(self.fontcombobox)
        layout.addWidget(self.lcdnumber)
        layout.addWidget(self.processbar)
        layout.addWidget(self.radiobutton)
        layout.addWidget(self.slider)
        layout.addWidget(self.spinbox)
        layout.addWidget(self.timeedit)

        container.setLayout(layout)

        self.setCentralWidget(container)

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
