from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QInputDialog, QRadioButton, QButtonGroup, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QFont, QMovie
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import os

class EncryptWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window  # Store the reference to MainWindow
        self.setWindowTitle("Encrypt Text")
        self.setGeometry(100, 100, 500, 450)
        self.setStyleSheet("background-color: black; color: white;")
        self.init_ui()
        QTimer.singleShot(0, self.center_window)

    def center_window(self):
        frame_geom = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        frame_geom.moveCenter(screen)
        self.move(frame_geom.topLeft())

    def init_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Encrypt Message")
        title.setFont(QFont("Times New Roman", 24, QFont.Bold))
        title.setAlignment(Qt.AlignHCenter)
        layout.addWidget(title)

        # Add GIF animation
        gif_label = QLabel(self)
        movie = QMovie("encrypt.gif")
        movie.setScaledSize(QSize(100, 100))
        gif_label.setMovie(movie)
        movie.start()
        gif_label.setAlignment(Qt.AlignHCenter)
        layout.addWidget(gif_label)

        # Encryption method selection
        choose_label = QLabel("Choose your encryption method:")
        choose_label.setFont(QFont("Times New Roman", 10))
        choose_label.setStyleSheet("color: #FFFDD0;")
        layout.addWidget(choose_label, alignment=Qt.AlignLeft)

        radio_layout = QHBoxLayout()
        self.fernet_radio = QRadioButton("Fernet")
        self.fernet_radio.setFont(QFont("Arial", 12))
        self.aes_radio = QRadioButton("AES")
        self.aes_radio.setFont(QFont("Arial", 12))
        self.caesar_radio = QRadioButton("Caesar Cipher")
        self.caesar_radio.setFont(QFont("Arial", 12))

        radio_layout.addWidget(self.fernet_radio)
        radio_layout.addWidget(self.aes_radio)
        radio_layout.addWidget(self.caesar_radio)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.fernet_radio)
        self.button_group.addButton(self.aes_radio)
        self.button_group.addButton(self.caesar_radio)

        self.fernet_radio.setStyleSheet("color: white;")
        self.aes_radio.setStyleSheet("color: white;")
        self.caesar_radio.setStyleSheet("color: white;")

        self.fernet_radio.toggled.connect(self.update_radio_color)
        self.aes_radio.toggled.connect(self.update_radio_color)
        self.caesar_radio.toggled.connect(self.update_radio_color)
        layout.addLayout(radio_layout)

        # Key input section
        key_label = QLabel("Enter your key:")
        key_label.setFont(QFont("Times New Roman", 12))
        layout.addWidget(key_label)

        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.setPlaceholderText("min 6 characters")
        self.key_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                font-family: 'Times New Roman';
                font-size: 12pt;
                padding: 10px 35px 10px 10px;
                border-radius: 15px;
            }
        """)

        from PyQt5.QtWidgets import QAction
        from PyQt5.QtGui import QIcon
        self.eye_open_icon = QIcon("eye_open.png")
        self.eye_closed_icon = QIcon("eye_close.png")
        self.toggle_visibility_action = QAction(self.eye_closed_icon, "", self.key_input)
        self.toggle_visibility_action.setCheckable(True)
        self.toggle_visibility_action.triggered.connect(self.toggle_key_visibility)
        self.key_input.addAction(self.toggle_visibility_action, QLineEdit.TrailingPosition)
        layout.addWidget(self.key_input)

        # Text input
        text_label = QLabel("Enter the text you want to encrypt:")
        text_label.setFont(QFont("Times New Roman", 12))
        layout.addWidget(text_label)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Type message here...")
        self.text_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                color: black;
                font-family: 'Times New Roman';
                font-size: 12pt;
                padding: 10px;
                border-radius: 15px;
            }
        """)
        layout.addWidget(self.text_input)

        # Encrypt Button
        encrypt_button = QPushButton("Encrypt & Save")
        encrypt_button.setFixedWidth(200)
        encrypt_button.setStyleSheet(self.encrypt_button_style())  # 🟰 use encrypt_button_style
        encrypt_button.clicked.connect(self.encrypt_text)
        layout.addSpacing(20)  
        layout.addWidget(encrypt_button, alignment=Qt.AlignCenter)

        # Result label
        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Times New Roman", 14))
        self.result_label.setWordWrap(True)
        layout.addWidget(self.result_label)

        # 👇 Back to Main Menu Button
        back_button = QPushButton("← Back to Main Menu")
        back_button.setFixedWidth(200)
        back_button.setStyleSheet(self.back_button_style())
        back_button.clicked.connect(self.go_back)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        # 🔥 Tip Label (closer to back button)
        tip_label = QLabel("💡 Tip: Always double-check before sharing your encrypted text!")
        tip_label.setFont(QFont("Arial", 10))
        tip_label.setStyleSheet("color: grey;")
        tip_label.setAlignment(Qt.AlignCenter)
        layout.addSpacing(5)  # small spacing only
        layout.addWidget(tip_label)

        self.setLayout(layout)



    def update_radio_color(self):
        # Reset all to white color
        self.fernet_radio.setStyleSheet("color: white;")
        self.aes_radio.setStyleSheet("color: white;")
        self.caesar_radio.setStyleSheet("color: white;")

        # Change the color of the selected radio button
        if self.fernet_radio.isChecked():
            self.fernet_radio.setStyleSheet("color: #00FF00;")  # Green for selected
        elif self.aes_radio.isChecked():
            self.aes_radio.setStyleSheet("color: #00FF00;")  # Green for selected
        elif self.caesar_radio.isChecked():
            self.caesar_radio.setStyleSheet("color: #00FF00;")  # Green for selected
            
    def encrypt_button_style(self):
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 teal, stop:1 white);
                color: black;
                padding: 10px;
                font-size: 16px;
                font-family: 'Segoe UI';
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #009999, stop:1 #e0f7f7);
            }
        """

    def back_button_style(self):
        return """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 red, stop:1 lightgrey);
                color: black;
                padding: 10px;
                font-size: 16px;
                font-family: 'Segoe UI';
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 darkred, stop:1 white);
            }
        """

        
    def go_back(self):
        self.close()  # Close the EncryptWindow
        if self.main_window:
            self.main_window.show()


    def button_style(self):
        return """
            QPushButton {
                background-color: teal;
                color: white;
                padding: 10px;
                font-size: 16px;
                font-family: 'Segoe UI';
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #009999;
            }
        """

    def generate_key(self, password):
        salt = b'\x00' * 16
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))

    def encrypt_fernet(self, key, message):
        fernet = Fernet(key)
        return fernet.encrypt(message.encode()).decode()

    def encrypt_aes(self, key, message):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padded_msg = self.pkcs7_pad(message.encode())
        encrypted = encryptor.update(padded_msg) + encryptor.finalize()
        return base64.urlsafe_b64encode(iv + encrypted).decode()

    def pkcs7_pad(self, data):
        block_size = 16
        padding_len = block_size - len(data) % block_size
        return data + bytes([padding_len] * padding_len)

    def encrypt_caesar(self, message, shift=3):
        result = ''
        for char in message:
            if char.isupper():
                result += chr((ord(char) - 65 + shift) % 26 + 65)
            elif char.islower():
                result += chr((ord(char) - 97 + shift) % 26 + 97)
            else:
                result += char
        return result

    from PyQt5.QtWidgets import QMessageBox

    def encrypt_text(self):
        key = self.key_input.text()
        message = self.text_input.text()

        if not message.strip():
            QMessageBox.warning(self, "Warning", "Please enter text to encrypt.")
            return

        try:
            if self.fernet_radio.isChecked():
                if len(key) < 6:
                    QMessageBox.warning(self, "Warning", "Key must be at least 6 characters.")
                    return
                fernet_key = self.generate_key(key)
                encrypted = self.encrypt_fernet(fernet_key, message)

            elif self.aes_radio.isChecked():
                if len(key) < 6:
                    QMessageBox.warning(self, "Warning", "Key must be at least 6 characters.")
                    return
                aes_key = self.generate_key(key)[:32]
                encrypted = self.encrypt_aes(aes_key, message)

            elif self.caesar_radio.isChecked():
                encrypted = self.encrypt_caesar(message, 3)

            else:
                QMessageBox.warning(self, "Warning", "Please select an encryption method.")
                return

            file_name, ok = QInputDialog.getText(self, "Save File", "Enter filename:")
            if ok and file_name.strip():
                # 🛠️ Save to 'encrypted_files' folder
                save_folder = os.path.join(os.getcwd(), "Encrypted_Files")
                os.makedirs(save_folder, exist_ok=True)
                path = os.path.join(save_folder, file_name + ".txt")

                with open(path, "w") as f:
                    f.write(encrypted)

                QMessageBox.information(self, "Success", f"Encryption Successful!")

                self.key_input.clear()
                self.text_input.clear()
            else:
                QMessageBox.information(self, "Cancelled", "Cancelled: No filename provided.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error: {str(e)}")



    def toggle_key_visibility(self):
        if self.toggle_visibility_action.isChecked():
            self.key_input.setEchoMode(QLineEdit.Normal)
            self.toggle_visibility_action.setIcon(self.eye_open_icon)
        else:
            self.key_input.setEchoMode(QLineEdit.Password)
            self.toggle_visibility_action.setIcon(self.eye_closed_icon)


            
import sys
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create and show the EncryptWindow
    encrypt_window = EncryptWindow()
    encrypt_window.show()
    
    # Run the application event loop
    sys.exit(app.exec_())
