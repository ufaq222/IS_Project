from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QGraphicsOpacityEffect, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtCore import QTimer
from image_ui import run_main_image_ui
from FileEncUI import FileEncryptionApp
from main import MainWindow
from PyQt5.QtGui import QMovie


class EncryptionPage(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setWindowTitle("Encryption / Decryption")
        self.parent_window = parent_window
        self.setFixedSize(600, 600)
        self.setStyleSheet("background-color: black;")  # Background color set to black
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

        self.widgets = []  # for animation

        # Title
        title = QLabel("Encryption and Decryption")
        title.setStyleSheet("color: #00FFC6; font-size: 28px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)
        self.widgets.append(title)
        
        # Add GIF under the title
        gif_label = QLabel(self)
        movie = QMovie("assets/encrypt.gif")  # Replace with the actual path to your GIF
        movie.setScaledSize(QSize(400, 200))  # Set desired width and height
        gif_label.setMovie(movie)
        gif_label.setAlignment(Qt.AlignCenter)  # Optional: center the GIF in the layout
        movie.start()  # Start the animation
        self.layout.addWidget(gif_label)
        self.widgets.append(gif_label)


        # Spacer to push buttons toward the center
        spacer_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer_top)

        # Create buttons with spacing between them
        self.widgets.append(self.create_button("Image Encryption/Decryption", "assets/image.svg", self.image_encryption))
        self.widgets.append(self.create_button("Text Encryption/Decryption", "assets/lock.svg", self.text_encryption))
        self.widgets.append(self.create_button("File Encryption/Decryption", "assets/lock.svg", self.file_encryption))

        # Add buttons with spacing between each
        for btn in self.widgets[1:]:
            self.layout.addWidget(btn)
            spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)  # 20px spacing between buttons
            self.layout.addItem(spacer)
            self.layout.setAlignment(btn, Qt.AlignCenter)


        # Spacer to keep the buttons centered vertically
        spacer_bottom = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding)  # Adjusted for bottom spacing
        self.layout.addItem(spacer_bottom)

        back_button = QPushButton("  Back")
        back_button.setFixedSize(360, 50)
        back_button.setIcon(QIcon("assets/back.svg"))
        back_button.setIconSize(QSize(24, 24))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                font-size: 16px;
                font-weight: 600;
                border-radius: 12px;
                padding: 8px 18px;
                text-align: left;
                border: 2px solid #E74C3C;
            }
            QPushButton:hover {
                background-color: #FF6B6B;
                border: 2px solid #FF6B6B;
            }
        """)
        back_button.clicked.connect(self.go_back)
        self.layout.addWidget(back_button)
        self.layout.setAlignment(back_button, Qt.AlignCenter)
        self.widgets.append(back_button)


        self.animate_widgets()

    def create_button(self, text, icon_path, func):
        btn = QPushButton(f"  {text}")
        btn.setFixedSize(360, 50)
        btn.setIcon(QIcon(icon_path))
        btn.setIconSize(QSize(24, 24))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #1ABC9C;
                color: white;
                font-size: 16px;
                font-weight: 600;
                border-radius: 12px;
                padding-left: 18px;
                padding-right: 18px;
                text-align: left;
                border: 2px solid #1ABC9C;
            }
            QPushButton:hover {
                background-color: #16A085;
                border: 2px solid #16A085;
            }
        """)
        btn.clicked.connect(func)
        return btn

    def animate_widgets(self):
        for i, widget in enumerate(self.widgets):
            opacity_effect = QGraphicsOpacityEffect()
            widget.setGraphicsEffect(opacity_effect)

            anim = QPropertyAnimation(opacity_effect, b"opacity")
            anim.setDuration(600)
            anim.setStartValue(0)
            anim.setEndValue(1)
            anim.setEasingCurve(QEasingCurve.InOutQuad)

            # Start animation with a delay using QTimer
            QTimer.singleShot(i * 150, anim.start)  # 150ms stagger between widgets

            # Prevent garbage collection
            widget._animation = anim

    def image_encryption(self):
        self.hide()
        self.image_page = run_main_image_ui(self)
        self.image_page.show()

    def text_encryption(self):
        print("Text Encryption/Decryption selected")
        self.hide()
        self.text_encryption_window = MainWindow(self)
        self.text_encryption_window.show()
        # Add the actual logic here
    def file_encryption(self):
        print("File Encryption/Decryption selected")
        self.hide()

        self.file_encryption_window = FileEncryptionApp()
        self.file_encryption_window.show()

    
    def go_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()
