from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QRadioButton, QHBoxLayout
from PyQt5.QtGui import QFont, QMovie
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import base64
import os
from PyQt5.QtWidgets import QFileDialog

class DecryptWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window # Store the reference to main window
        self.setWindowTitle("Decrypt Text")
        self.setGeometry(100, 100, 500, 500)  # Adjusted to fit the gif and additional space
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
        layout.setSpacing(20)

        # 🏷 Title
        title = QLabel("Decrypt Message")
        title.setFont(QFont("Times New Roman", 22, QFont.Bold))
        title.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        layout.addWidget(title)

        # 🖼 GIF Display (Now placed after the label)
        self.gif_label = QLabel()
        self.movie = QMovie("decrypt.gif")  # Provide the path to your GIF
        self.gif_label.setMovie(self.movie)
        self.gif_label.setFixedSize(100, 100)  # Adjust size as needed
        self.gif_label.setAlignment(Qt.AlignCenter)  # Ensures GIF is centered in its space
        self.movie.start()
        layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)
        
        # New Label to select the encryption method
        method_label = QLabel("Choose the encryption method:")
        method_label.setFont(QFont("Times New Roman", 13))
        method_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(method_label)

        # Encryption Method Radio Buttons (in a horizontal layout)
        radio_layout = QHBoxLayout()
        self.fernet_radio = QRadioButton("Fernet")
        self.aes_radio = QRadioButton("AES")
        self.caesar_radio = QRadioButton("Caesar Cipher")
        
        # Set the radio buttons to not have any selected by default
        self.fernet_radio.setChecked(False)
        self.aes_radio.setChecked(False)
        self.caesar_radio.setChecked(False)
        
        # Set the font size of the options to make them a little bigger
        font = QFont("Times New Roman", 14)
        self.fernet_radio.setFont(font)
        self.aes_radio.setFont(font)
        self.caesar_radio.setFont(font)

        # Add radio buttons to the horizontal layout
        radio_layout.addWidget(self.fernet_radio)
        radio_layout.addWidget(self.aes_radio)
        radio_layout.addWidget(self.caesar_radio)

        layout.addLayout(radio_layout)
        
        # New layout for label and button side by side
        choose_layout = QHBoxLayout()
        choose_label = QLabel("Choose text you want to decrypt:")
        choose_label.setFont(QFont("Times New Roman", 14))
        choose_label.setAlignment(Qt.AlignLeft)
        choose_layout.addWidget(choose_label, stretch=2)

        choose_button = QPushButton("Choose Text")
        choose_button.clicked.connect(self.choose_text)
        choose_button.setFixedWidth(150)
        choose_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #800080,  /* purple */
                    stop: 1 #808080   /* grey */
                );
                color: white;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI';
                border: 2px solid #800080;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #9932CC,
                    stop: 1 #A9A9A9
                );
                color: white;
                border: 2px solid white;
            }
            QPushButton:pressed {
                background-color: #4B0082;
                color: white;
            }
        """)

        choose_layout.addWidget(choose_button, alignment=Qt.AlignRight, stretch=1)
        layout.addLayout(choose_layout)

        # 🗝 Key Input (Password field)
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.Password)
        self.key_input.setPlaceholderText("Enter key used for encryption")
        self.key_input.setStyleSheet(self.input_style())
        layout.addWidget(self.key_input)

        # 🔒 Encrypted Message Input
        self.encrypted_input = QLineEdit()
        self.encrypted_input.setPlaceholderText("Paste encrypted message here")
        self.encrypted_input.setStyleSheet(self.input_style())
        layout.addWidget(self.encrypted_input)

        # 📲 Decrypt Button
        decrypt_button = QPushButton("Decrypt")
        decrypt_button.setFixedWidth(200)
        decrypt_button.setStyleSheet(self.button_style())
        decrypt_button.clicked.connect(self.decrypt_text)
        layout.addWidget(decrypt_button, alignment=Qt.AlignCenter)
        
        # 🛑 Back Button
        back_button = QPushButton("← Back to Main Menu")
        back_button.setFixedWidth(200)
        back_button.setStyleSheet(self.back_button_style())
        back_button.clicked.connect(self.go_back)  # Connect the Back button to go_back
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        # 🗯 Decrypted Message Display Box (with teal border)
        self.decrypted_box = QWidget()
        self.decrypted_box.setStyleSheet("""
            QWidget {
                border: 2px solid teal;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.decrypted_message = QLabel("Decrypted message will appear here")
        self.decrypted_message.setAlignment(Qt.AlignCenter)
        self.decrypted_message.setFont(QFont("Times New Roman", 14))
        self.decrypted_box_layout = QVBoxLayout(self.decrypted_box)
        self.decrypted_box_layout.addWidget(self.decrypted_message)

        layout.addWidget(self.decrypted_box)

        # 💡 Helpful Tip Label with Icon
        tip_label = QLabel("💡 Tip: Choose the same decryption method you choose during encryption time!")
        tip_label.setAlignment(Qt.AlignHCenter)
        tip_label.setStyleSheet("""
            color: lightgray;
            font-size: 10px;
            font-style: italic;
            padding-top: 5px;
        """)
        layout.addWidget(tip_label)

        self.setLayout(layout)


    
    def go_back(self):
        self.close()  # Close the EncryptWindow
        print("smbmmsbm")
        if self.main_window:
            self.main_window.show()
        else:
            print("KKKKKKKKKKK")
                

        

    def combo_style(self):
        return """
            QComboBox {
                background-color: white;
                color: black;
                padding: 10px;
                font-size: 16px;
                font-family: 'Segoe UI';
                border: 2px solid teal;
                border-radius: 12px;
            }
            QComboBox:hover {
                border-color: #009999;
            }
        """

    def input_style(self):
        return """
            QLineEdit {
                background-color: white;
                color: black;
                padding: 8px;
                font-size: 14px;
                font-family: 'Segoe UI';
                border-radius: 10px;
                border: 2px solid teal;
            }
            QLineEdit:hover {
                border-color: #009999;
            }
        """

    def button_style(self):
        return """
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 teal,
                    stop: 1 white
                );
                color: black;
                padding: 10px;
                font-size: 14px;
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
        
        
    def back_button_style(self):
        return """
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #FF6347,  /* Tomato red */
                    stop: 1 #808080   /* Grey */
                );
                color: black;
                padding: 10px;
                font-size: 14px;
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
    

    def generate_key(self, password):
        salt = b'\x00' * 16
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def choose_text(self):
        encrypted_folder = "Encrypted_Files"  # folder where encrypted files are stored
        
        # Make sure the folder exists
        if not os.path.exists(encrypted_folder):
            self.result_label.setText("Encrypted folder not found.")
            return

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        
        # Open dialog in the encrypted_folder, showing only .txt files
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Choose Encrypted Text File",
            encrypted_folder,
            "Text Files (*.txt)",
            options=options
        )
        
        if file_name:
            with open(file_name, 'r') as file:
                content = file.read()
                self.encrypted_input.setText(content)

    def decrypt_fernet(self, key, message):
        fernet = Fernet(key)
        return fernet.decrypt(message.encode()).decode()

    def decrypt_aes(self, key, message):
        raw = base64.urlsafe_b64decode(message.encode())
        iv = raw[:16]
        ciphertext = raw[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()
        pad_len = decrypted[-1]
        return decrypted[:-pad_len].decode()

    def decrypt_caesar(self, message, shift=3):
        result = ''
        for char in message:
            if char.isupper():
                result += chr((ord(char) - 65 - shift) % 26 + 65)
            elif char.islower():
                result += chr((ord(char) - 97 - shift) % 26 + 97)
            else:
                result += char
        return result

    def decrypt_text(self):
        key = self.key_input.text()
        message = self.encrypted_input.text()

        if not message.strip():
            self.decrypted_message.setText("Please enter an encrypted message.")
            return

        # 🔥 Correct way to detect selected encryption method
        if self.fernet_radio.isChecked():
            method = "Fernet"
        elif self.aes_radio.isChecked():
            method = "AES"
        elif self.caesar_radio.isChecked():
            method = "Caesar Cipher"
        else:
            self.decrypted_message.setText("Please select an encryption method.")
            return

        try:
            if method == "Fernet":
                if len(key) < 6:
                    self.decrypted_message.setText("Key must be at least 6 characters.")
                    return
                fernet_key = self.generate_key(key)
                decrypted = self.decrypt_fernet(fernet_key, message)

            elif method == "AES":
                if len(key) < 6:
                    self.decrypted_message.setText("Key must be at least 6 characters.")
                    return
                aes_key = self.generate_key(key)[:32]  # AES needs exactly 32 bytes
                decrypted = self.decrypt_aes(aes_key, message)

            elif method == "Caesar Cipher":
                shift = 3  # default Caesar shift
                decrypted = self.decrypt_caesar(message, shift)

            else:
                self.decrypted_message.setText("Unsupported method selected.")
                return

            self.decrypted_message.setText(f"Decrypted Message:\n{decrypted}")

        except Exception as e:
            self.decrypted_message.setText("Error: Invalid key or message or method.")


            
            
            
          
