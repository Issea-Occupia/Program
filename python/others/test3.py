from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QRect, QRectF
from PyQt6.QtGui import QColor, QPainter, QBrush, QPainterPath

class FancyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✨ PyQt6 华丽交互示例 ✨")
        self.resize(500, 300)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton("✨ Click Me ✨", self)
        self.button.setFixedSize(200, 60)
        self.button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #7A7FFF, stop:1 #4A4AFF);
                border: none;
                border-radius: 30px;
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #9A9FFF, stop:1 #6A6AFF);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #4A4AFF, stop:1 #2A2AFF);
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 6)
        self.button.setGraphicsEffect(shadow)

        layout.addWidget(self.button)
        self.button.clicked.connect(self.play_click_animation)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rectf = QRectF(self.rect())            # ← 关键修复：转成 QRectF
        path = QPainterPath()
        path.addRoundedRect(rectf, 20.0, 20.0) # 半径用 float 更稳
        painter.fillPath(path, QBrush(QColor(255, 255, 255, 30)))

    def play_click_animation(self):
        geom = self.button.geometry()
        anim = QPropertyAnimation(self.button, b"geometry")
        anim.setDuration(150)
        anim.setEasingCurve(QEasingCurve.Type.OutBounce)
        anim.setStartValue(geom)
        anim.setEndValue(QRect(geom.x(), geom.y() - 5, geom.width(), geom.height()))
        anim.start()
        self.anim = anim  # 防止被回收

if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("Fusion")
    w = FancyWindow()
    w.show()
    app.exec()
