import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QMessageBox,
    QGraphicsDropShadowEffect, QHBoxLayout, QFrame, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QIcon, QPainter, QLinearGradient, QBrush, QColor, QMovie

from utils import center_window
from encryption_ui import EncryptionPage
from password_ui import PasswordUI


class CustomExitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Exit")
        self.setFixedSize(300, 120)
        layout = QVBoxLayout()
        label = QLabel("Are you sure you want to exit?")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        buttons = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        self.setLayout(layout)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Information Security Project")
        self.setFixedSize(600, 550)
        self.setAttribute(Qt.WA_TranslucentBackground)
        center_window(self, 600, 550)

        self.init_ui()
        self.animate_window()

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#000000"))
        gradient.setColorAt(1, QColor("#000000"))
        painter.fillRect(self.rect(), QBrush(gradient))

    def animate_window(self):
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(700)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        self.anim.setStartValue(QRect(self.x(), self.y() + 100, self.width(), self.height()))
        self.anim.setEndValue(QRect(self.x(), self.y(), self.width(), self.height()))
        self.anim.start()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        glass_frame = QFrame(self)
        glass_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.08);
                border-radius: 18px;
            }
        """)
        glass_frame.setGeometry(40, 20, 520, 500)

        glass_layout = QVBoxLayout(glass_frame)
        glass_layout.setAlignment(Qt.AlignCenter)

        title = QLabel("\U0001F4BB IS Project")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #00FFC6; font-size: 32px; font-weight: bold;")
        glass_layout.addWidget(title)
        glass_layout.addSpacing(15)

        gif = QLabel()
        movie = QMovie("assets/Security-Lock.gif")
        movie.setScaledSize(QSize(200, 150))
        gif.setMovie(movie)
        gif.setAlignment(Qt.AlignCenter)
        movie.start()
        glass_layout.addWidget(gif)
        glass_layout.addSpacing(35)

        glass_layout.addWidget(self.make_button("Encryption / Decryption", "assets/lock.svg", self.open_encryption))
        glass_layout.addSpacing(15)
        glass_layout.addWidget(self.make_button("Password Strength Analyzer", "assets/lock.svg", self.open_password))
        glass_layout.addSpacing(30)
        glass_layout.addWidget(self.make_button("Exit", "assets/exit.svg", self.confirm_exit, red=True))

        layout.addWidget(glass_frame)

    def make_button(self, text, icon_path, func, red=False):
        btn = QPushButton(f"  {text}")
        btn.setFixedSize(360, 50)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(24, 24))
        btn.setCursor(Qt.PointingHandCursor)

        btn.setGraphicsEffect(QGraphicsDropShadowEffect(
            blurRadius=12, xOffset=0, yOffset=2, color=QColor(0, 255, 200, 80)))

        base_color = "#E74C3C" if red else "#1ABC9C"
        hover_color = "#FF6B6B" if red else "#16A085"

        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {base_color};
                color: white;
                font-size: 16px;
                font-weight: 600;
                border-radius: 12px;
                padding-left: 18px;
                text-align: left;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                color: #FFFACD;
            }}
        """)
        btn.clicked.connect(func)
        return btn

    def open_encryption(self):
        self.enc_win = EncryptionPage(parent_window=self)
        self.enc_win.show()
        self.hide()

    def open_password(self):
        self.pwd_win = PasswordUI(parent_window=self)
        self.pwd_win.show()
        self.hide()

    def confirm_exit(self):
        dlg = CustomExitDialog(self)
        if dlg.exec_():
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
