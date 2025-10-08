from PyQt6.QtWidgets import QLineEdit,QMainWindow,QApplication
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.lineedit = QLineEdit()
        self.lineedit.setMaxLength(20)
        maxlen = self.lineedit.maxLength()

        self.lineedit.setPlaceholderText("type your name:")
        placetext = self.lineedit.placeholderText()
        self.lineedit.returnPressed.connect(self.return_pressed)
        self.lineedit.selectionChanged.connect(self.selection_changed)
        self.lineedit.textChanged.connect(self.text_changed)
        self.lineedit.textEdited.connect(self.text_edited)

        self.setCentralWidget(self.lineedit)

    def return_pressed(self):
        print("Return pressed!")
        self.centralWidget().setText("boom")

    def selection_changed(self):
        print("Selection changed")
    
    def text_changed(self):
        print("Text changed...")

    def text_edited(self):
        print("Text edited...")

app = QApplication([])
window = MainWindow()
window.show()
app.exec()