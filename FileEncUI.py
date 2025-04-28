import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QWidget, QVBoxLayout, QLabel, QPushButton,
    QTabWidget, QLineEdit, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy

import FileEnc as core


class FileDropLabel(QLabel):
    def __init__(self, default_text, parent=None):
        super().__init__(default_text, parent)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px dashed #2EA6FF; padding: 12px; font-size: 13px;")
        self.setWordWrap(True)
        self.file_path = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.setText(file_path)
            self.file_path = file_path


class FileEncryptionApp(QMainWindow):
    def __init__(self, parent_window=None):
        super().__init__()
        self.parent_window = parent_window  # Store parent reference
        self.setWindowTitle("Secure File Vault")
        self.setGeometry(300, 100, 700, 500)
        self.setWindowIcon(QIcon("lock.png"))

        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #000000;
            }
            QPushButton {
                background-color: #3a3a3a;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QLineEdit {
                background-color: #222;
                color: white;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 6px;
            }
            QLabel {
                color: white;
            }
        """)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Top layout with tabs and home button
        top_layout = QHBoxLayout()

        # Adding the tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabWidget::pane { border: none; }")
        top_layout.addWidget(self.tabs)

    
        
        self.home_button = QPushButton("EXIT")
        self.home_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: Red;
                font-size: 10px;
                font-weight: bold;
                border-radius: 0px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)


        
        self.home_button.clicked.connect(self.go_home)
        top_layout.addWidget(self.home_button, alignment=Qt.AlignTop)

        layout.addLayout(top_layout)

        # Create the tabs content
        self.encrypt_tab = QWidget()
        self.decrypt_tab = QWidget()
        self.key_tab = QWidget()

        self.tabs.addTab(self.encrypt_tab, "🔐 Encrypt")
        self.tabs.addTab(self.decrypt_tab, "🔓 Decrypt")
        self.tabs.addTab(self.key_tab, "🗝️ Key Management")

        # Initialize the tabs' contents
        self.init_encrypt_tab()
        self.init_decrypt_tab()
        self.init_key_tab()
        
    def create_page_layout(self, title):
        layout = QVBoxLayout()
        heading = QLabel(title)
        heading.setAlignment(Qt.AlignCenter)
        heading.setFont(QFont("Times New Roman", 16, QFont.Bold))
        heading.setStyleSheet("""
            margin-top: 60px;
            margin-bottom: 15px;
        """)
        layout.addWidget(heading)
        return layout

    def init_encrypt_tab(self):
        layout = self.create_page_layout("File Encryption Menu")

        self.enc_file_label = FileDropLabel("Drop a file here or use the button below.")
        self.enc_select_btn = QPushButton("📂 Choose File to Encrypt")
        self.enc_select_btn.clicked.connect(self.select_encrypt_file)

        key_layout = QHBoxLayout()
        self.public_key_path = QLineEdit()
        self.public_key_path.setPlaceholderText("Path to recipient's public key (.pem)")
        self.enc_key_browse = QPushButton("📁 Browse Public Key")
        self.enc_key_browse.clicked.connect(lambda: self.load_key_file(self.public_key_path))
        key_layout.addWidget(self.public_key_path)
        key_layout.addWidget(self.enc_key_browse)

        self.encrypt_btn = QPushButton("🔐 Encrypt")
        self.encrypt_btn.clicked.connect(self.encrypt_file)
        self.encrypt_btn.setStyleSheet("background-color: #4682B4; color: white;")

        info = QLabel("💡 Tip: You can also drag and drop your file above.")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: gray; font-style: italic; margin-top: 12px;")

        layout.addWidget(self.enc_file_label)
        layout.addWidget(self.enc_select_btn)
        layout.addLayout(key_layout)
        layout.addWidget(self.encrypt_btn)
        layout.addWidget(info)

        self.encrypt_tab.setLayout(layout)

    def init_decrypt_tab(self):
        layout = self.create_page_layout("File Decryption Menu")

        self.dec_file_label = FileDropLabel("Drop the encrypted file here or use the button below.")
        self.dec_select_btn = QPushButton("📂 Choose Encrypted File")
        self.dec_select_btn.clicked.connect(self.select_decrypt_file)

        key_layout = QHBoxLayout()
        self.private_key_path = QLineEdit()
        self.private_key_path.setPlaceholderText("Path to your private key (.pem)")
        self.dec_key_browse = QPushButton("📁 Browse Private Key")
        self.dec_key_browse.clicked.connect(lambda: self.load_key_file(self.private_key_path))
        key_layout.addWidget(self.private_key_path)
        key_layout.addWidget(self.dec_key_browse)

        self.decrypt_btn = QPushButton("🔓 Decrypt")
        self.decrypt_btn.clicked.connect(self.decrypt_file)

        info = QLabel("💡 Tip: You can also drag and drop your encrypted file above.")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: gray; font-style: italic; margin-top: 12px;")

        layout.addWidget(self.dec_file_label)
        layout.addWidget(self.dec_select_btn)
        layout.addLayout(key_layout)
        layout.addWidget(self.decrypt_btn)
        layout.addWidget(info)

        self.decrypt_tab.setLayout(layout)

    def init_key_tab(self):
        layout = self.create_page_layout("RSA Key Management")
        self.key_status = QLabel("To Generate RSA Key Pair click on the button below!")
        self.key_status.setFont(QFont("Times New Roman", 10))
        layout.addSpacing(50)

        self.gen_keys_btn = QPushButton("🗝️ Generate RSA Keypair")
        self.gen_keys_btn.clicked.connect(self.generate_keys)

        info = QLabel("Generates a pair of RSA keys (public and private) and saves them.")
        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("color: gray; font-style: italic; margin-top: 12px;")

        layout.addWidget(self.key_status)
        layout.addWidget(self.gen_keys_btn)
        layout.addStretch(9)
        layout.addWidget(info)

        self.key_tab.setLayout(layout)

    def load_key_file(self, line_edit):
        path, _ = QFileDialog.getOpenFileName(self, "Select Key File")
        if path:
            line_edit.setText(path)

    def select_encrypt_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File to Encrypt")
        if path:
            self.enc_file_label.setText(path)
            self.enc_file_label.file_path = path

    def select_decrypt_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File to Decrypt")
        if path:
            self.dec_file_label.setText(path)
            self.dec_file_label.file_path = path

    def encrypt_file(self):
        file_path = self.enc_file_label.file_path
        pub_key_path = self.public_key_path.text()
        try:
            pub_key = core.load_public_key(pub_key_path)
            output = core.encrypt_file_rsa(file_path, pub_key)
            QMessageBox.information(self, "Success", f"Encrypted file saved as:\n{output}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def decrypt_file(self):
        file_path = self.dec_file_label.file_path
        priv_key_path = self.private_key_path.text()
        try:
            priv_key = core.load_private_key(priv_key_path)
            output = core.decrypt_file_rsa(file_path, priv_key)
            QMessageBox.information(self, "Success", f"Decrypted file saved as:\n{output}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def generate_keys(self):
        priv_key, pub_key = core.generate_rsa_keypair()
        priv_path, _ = QFileDialog.getSaveFileName(self, "Save Private Key", filter="*.pem")
        pub_path, _ = QFileDialog.getSaveFileName(self, "Save Public Key", filter="*.pem")
        if priv_path and pub_path:
            core.save_rsa_keys(priv_key, pub_key, priv_path, pub_path)
            self.key_status.setText("RSA Keypair saved successfully.")
        else:
            self.key_status.setText("Key generation canceled.")

    def go_home(self):
        from ui import MainWindow  # Import only when needed
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    dark_palette = QPalette()
    dark_palette.setColor(QPalette.Window, QColor(0, 0, 0))
    dark_palette.setColor(QPalette.WindowText, Qt.white)
    dark_palette.setColor(QPalette.Base, QColor(20, 20, 20))
    dark_palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
    dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
    dark_palette.setColor(QPalette.ToolTipText, Qt.white)
    dark_palette.setColor(QPalette.Text, Qt.white)
    dark_palette.setColor(QPalette.Button, QColor(60, 60, 60))
    dark_palette.setColor(QPalette.ButtonText, Qt.white)
    dark_palette.setColor(QPalette.BrightText, Qt.red)
    dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    dark_palette.setColor(QPalette.HighlightedText, Qt.black)
    app.setPalette(dark_palette)
    from ui import MainWindow

    home_window = MainWindow()
    window = FileEncryptionApp(parent_window=home_window)
    window.show()
    sys.exit(app.exec_())
