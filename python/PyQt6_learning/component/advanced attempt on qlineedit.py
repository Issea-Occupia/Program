from PyQt6.QtWidgets import QLineEdit,QApplication,QMainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QLineEdit()
        self.widget.setText("please type your name")

