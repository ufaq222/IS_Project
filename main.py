import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QMovie
from encrypt_ui import EncryptWindow
from decrypt_ui import DecryptWindow


class MainWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 500, 400)
        self.setStyleSheet("background-color: black; color: white;")
        self.init_ui()
        QTimer.singleShot(0, self.center_window)

    def center_window(self):
        frame_geom = self.frameGeometry()
        screen = QApplication.primaryScreen().availableGeometry().center()
        frame_geom.moveCenter(screen)
        self.move(frame_geom.topLeft())

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # 🏷 Title
        title = QLabel("Text Encryption")
        title.setFont(QFont("Times New Roman", 24, QFont.Bold))
        title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(title)

        # 📽 Animated GIF - Centered
        gif_container = QVBoxLayout()
        gif_container.setAlignment(Qt.AlignHCenter)

        gif_label = QLabel()
        gif_label.setFixedSize(150, 150)
        gif_label.setAlignment(Qt.AlignCenter)

        movie = QMovie("animation.gif")
        movie.setScaledSize(gif_label.size())
        gif_label.setMovie(movie)
        movie.start()

        gif_container.addWidget(gif_label)
        layout.addLayout(gif_container)


        # 📦 Buttons
        btn_layout = QVBoxLayout()
        btn_layout.setAlignment(Qt.AlignHCenter)

        encrypt_btn = QPushButton("Encrypt")
        encrypt_btn.setFixedWidth(200)
        encrypt_btn.setStyleSheet(self.button_style())
        encrypt_btn.clicked.connect(self.open_encrypt)
        btn_layout.addWidget(encrypt_btn)

        decrypt_btn = QPushButton("Decrypt")
        decrypt_btn.setFixedWidth(200)
        decrypt_btn.setStyleSheet(self.button_style())
        decrypt_btn.clicked.connect(self.open_decrypt)
        btn_layout.addWidget(decrypt_btn)
        
        back_btn = QPushButton("<- Back")
        back_btn.setFixedWidth(200)
        back_btn.setStyleSheet(self.back_button_style())
        back_btn.clicked.connect(self.go_back)
        btn_layout.addWidget(back_btn)

        layout.addLayout(btn_layout)

        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)
        
        # 💡 Helpful Tip Label with Icon
        tip_label = QLabel("💡 Tip: Choose an action to get started — encryption keeps your text safe, decryption unlocks it!")
        tip_label.setAlignment(Qt.AlignHCenter)
        tip_label.setStyleSheet("""
            color: lightgray;
            font-size: 10px;
            font-style: italic;
            padding-top: 5px;
        """)
        layout.addWidget(tip_label)


    def button_style(self):
        return """
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 teal,
                    stop: 1 white
                );
                color: black;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
                border: 2px solid teal;
                border-radius: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #008080,
                    stop: 1 #ccffff
                );
                color: white;
                border: 2px solid white;
            }
            QPushButton:pressed {
                background-color: #004d4d;
                color: white;
            }
        """

    def go_back(self):
        self.close()  # Close the EncryptWindow
        if self.main_window:
            self.main_window.show()
            
            
    def back_button_style(self):
        return """
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #FF6347,  /* Tomato red */
                    stop: 1 #808080   /* Grey */
                );
                color: black;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI';
                border: 2px solid #FF6347;   /* Red border to match the background */
                border-radius: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #B22222,  /* Firebrick red */
                    stop: 1 #d3d3d3   /* Lighter grey */
                );
                color: white;
                border: 2px solid white;
            }
            QPushButton:pressed {
                background-color: #8B0000;  /* Dark red */
                color: white;
            }
        """
        
    def open_encrypt(self):
        self.close()  # Close the main window
        self.encrypt_window = EncryptWindow(main_window=self)  # Pass reference to the main window
        self.encrypt_window.show()

    def open_decrypt(self):
        self.close()  # Close the main window
        self.decrypt_window = DecryptWindow(main_window=self)  # Assuming DecryptWindow does not need main_window reference
        self.decrypt_window.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
