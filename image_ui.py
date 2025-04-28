from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QSpacerItem, QSizePolicy, QGraphicsOpacityEffect
)
from PyQt5.QtGui import QIcon, QMovie, QFont
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, QRect, QTimer
import sys
from image_encryption_ui import run_encryption_ui
from image_decryption_ui import run_decryption_ui

def animate_widget_opacity(widget, duration=1000, delay=0):
    effect = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(effect)
    animation = QPropertyAnimation(effect, b"opacity")
    animation.setDuration(duration)
    animation.setStartValue(0)
    animation.setEndValue(1)
    animation.setEasingCurve(QEasingCurve.InOutQuad)
    
    # Store the animation to prevent it from being garbage collected
    widget._opacity_animation = animation

    if delay:
        QTimer.singleShot(delay, animation.start)
    else:
        animation.start()


def animate_widget_slide(widget, start_rect, end_rect, duration=1000, delay=0):
    widget.setGeometry(start_rect)
    animation = QPropertyAnimation(widget, b"geometry")
    animation.setDuration(duration)
    animation.setStartValue(start_rect)
    animation.setEndValue(end_rect)
    animation.setEasingCurve(QEasingCurve.OutBack)
    
    # Store the animation to prevent it from being garbage collected
    widget._slide_animation = animation

    if delay:
        QTimer.singleShot(delay, animation.start)
    else:
        animation.start()

def run_main_image_ui(parent_window=None):
    app = QApplication.instance() or QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("Image Security Hub")
    window.setFixedSize(520, 470)
    window.setWindowIcon(QIcon('icon.png'))

    window.setStyleSheet("""
        QWidget {
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 black, stop:1 #1C1C1C);
            color: white;
            font-family: 'Segoe UI', sans-serif;
        }
        QPushButton {
            font-size: 17px;
            border-radius: 12px;
            padding: 12px;
            font-weight: bold;
            border: none;
            transition: all 0.2s ease-in-out;
        }
        QPushButton:hover {
            background-color: #34495E;
        }
    """)

    layout = QVBoxLayout()
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(20)

    # Title
    title = QLabel("\U0001F510 Image Encryption & Decryption Hub")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 24px; font-weight: bold; color: #00BCD4;")
    animate_widget_opacity(title, 1200)
    layout.addWidget(title)

    # GIF below title
    gif_label = QLabel()
    gif_label.setAlignment(Qt.AlignCenter)
    gif = QMovie("assets/key.gif")
    gif.setScaledSize(QSize(150, 150))
    gif_label.setMovie(gif)
    gif.start()
    layout.addWidget(gif_label)
    animate_widget_slide(gif_label, QRect(185, -150, 150, 150), QRect(185, 80, 150, 150), 1000)

    layout.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

    # Buttons
    buttons = []

    encrypt_btn = QPushButton("\U0001F512 Image Encryption")
    encrypt_btn.setStyleSheet("background-color: #008080; color: white;")
    encrypt_btn.setIcon(QIcon("encrypt_icon.png"))
    encrypt_btn.clicked.connect(lambda: (window.close(), run_encryption_ui(window)))
    layout.addWidget(encrypt_btn)
    buttons.append(encrypt_btn)

    decrypt_btn = QPushButton("\U0001F513 Image Decryption")
    decrypt_btn.setStyleSheet("background-color: #27AE60; color: white;")
    decrypt_btn.setIcon(QIcon("decrypt_icon.png"))
    decrypt_btn.clicked.connect(lambda: (window.close(), run_decryption_ui(window)))
    layout.addWidget(decrypt_btn)
    buttons.append(decrypt_btn)

    back_btn = QPushButton("\u2B05 Back")
    back_btn.setStyleSheet("background-color: #E74C3C; color: white;")
    back_btn.setIcon(QIcon("back_icon.png"))
    back_btn.clicked.connect(lambda: (window.close(), parent_window.show() if parent_window else None))
    layout.addWidget(back_btn)
    buttons.append(back_btn)

    # Animate Buttons
    for i, btn in enumerate(buttons):
        QTimer.singleShot(500 + i * 200, lambda b=btn: animate_widget_opacity(b, 500))

    layout.addSpacerItem(QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
    window.setLayout(layout)

    if parent_window:
        parent_window.hide()

    window.show()
    return window
