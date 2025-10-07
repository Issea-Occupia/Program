from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import sys

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("按钮切换图片显示")
        self.resize(400, 300)

        self.label = QLabel()
        pixmap = QPixmap(r"C:\Users\Issea Occupia\Desktop\QQ图片20251004212100.png")
        self.label.setPixmap(pixmap)
        self.label.setScaledContents(True)

        self.button = QPushButton("隐藏图片")
        self.button.clicked.connect(self.toggle_image)

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def toggle_image(self):
        visible = self.label.isVisible()
        self.label.setVisible(not visible)
        self.button.setText("显示图片" if visible else "隐藏图片")

app = QApplication(sys.argv)
window = MyWindow()
window.show()
app.exec()
