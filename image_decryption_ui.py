from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog, QMessageBox,
    QVBoxLayout, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy,
    QComboBox, QInputDialog, QLineEdit, QRadioButton
)
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter, QMovie, QPixmap
from PyQt5.QtCore import Qt, QSize
import image

decrypted_output_path = None
encrypted_image_path = None
current_algorithm = "AES"  # Default algorithm

def select_encrypted_image_for_decryption(label):
    global encrypted_image_path
    encrypted_image_path, _ = QFileDialog.getOpenFileName(
        None, 
        "Select Encrypted Image", 
        "", 
        "Encrypted Files (*.enc)"
    )
    if encrypted_image_path:
        label.setText(f"📁 {encrypted_image_path.split('/')[-1]}")

def decrypt_image_ui(parent=None):
    global encrypted_image_path, current_algorithm
    
    if not encrypted_image_path:
        QMessageBox.warning(parent, "Error", "Please select an encrypted image file.")
        return
    
    password, ok = QInputDialog.getText(
        parent, 
        'Password', 
        'Enter decryption password:', 
        QLineEdit.Password
    )
    if not ok or not password:
        return
    
    output_path, _ = QFileDialog.getSaveFileName(
        None, 
        "Save Decrypted Image As", 
        "", 
        "PNG Files (*.png)"
    )
    if not output_path:
        return
    
    try:
        success = False
        if current_algorithm == "AES":
            success = image.decrypt_image_aes(encrypted_image_path, output_path, password)
        elif current_algorithm == "ChaCha20":
            success = image.decrypt_image_chacha20(encrypted_image_path, output_path, password)
        elif current_algorithm == "Fernet":
            success = image.decrypt_image_fernet(encrypted_image_path, output_path, password)
        
        if success:
            QMessageBox.information(
                parent, 
                "Success", 
                f"✅ Image decrypted successfully!\nSaved to: {output_path}"
            )
        else:
            QMessageBox.warning(
                parent, 
                "Error", 
                "Decryption failed. Incorrect password or corrupted file."
            )
    except Exception as e:
        QMessageBox.critical(
            parent, 
            "Error", 
            f"❌ Failed to decrypt the image: {str(e)}"
        )

def create_button(text, icon_path, function, icon_size=20, button_style=None):
    button = QPushButton(f"  {text}")
    button.setCursor(Qt.PointingHandCursor)
    button.setIcon(QIcon(icon_path))
    button.setIconSize(QSize(icon_size, icon_size))
    button.clicked.connect(function)
    if button_style:
        button.setStyleSheet(button_style)
    return button

class GlassFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        color = QColor(30, 30, 30, 160)  # semi-transparent black
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)
        super().paintEvent(event)

def run_decryption_ui(parent_window=None):
    global current_algorithm
    
    window = QWidget()
    window.setWindowTitle("🔓 Image Decryption")
    window.setStyleSheet("""
        QWidget {
            background-color: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:1,
                stop:0 #0f2027, stop:0.5 #203a43, stop:1 #2c5364
            );
            color: #ECECEC;
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            font-size: 15px;
        }
        QLabel {
            font-size: 16px;
            font-weight: 500;
        }
        QPushButton {
            background-color: #34495E;
            color: white;
            padding: 8px 24px;
            border-radius: 12px;
            font-size: 15px;
            font-weight: 600;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
            border: 1px solid #3E5871;
        }
        QPushButton:hover {
            background-color: #3E5871;
            border: 1px solid #5D7B9D;
        }
        QComboBox {
            background-color: #34495E;
            color: white;
            padding: 8px;
            border-radius: 12px;
            border: 1px solid #3E5871;
            min-width: 120px;
        }
        QComboBox:hover {
            background-color: #3E5871;
        }
    """)
    window.setFixedSize(640, 600)

    layout = QVBoxLayout(window)
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(25)

    title = QLabel("🔓 Decrypt Your Image")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 26px; font-weight: bold; color: #1ABC9C; letter-spacing: 1px;")
    layout.addWidget(title)
    
    gif_label = QLabel()
    gif_label.setAlignment(Qt.AlignCenter)
    gif = QMovie("assets/image_decryption.gif")  # Make sure this path is correct
    gif.setScaledSize(QSize(250, 200))
    gif_label.setMovie(gif)
    gif.start()
    layout.addWidget(gif_label)

    card = GlassFrame()
    vbox = QVBoxLayout(card)
    vbox.setSpacing(20)

    # Algorithm selection (Radio buttons)
    aes_radio = QRadioButton("AES")
    aes_radio.setChecked(current_algorithm == "AES")
    aes_radio.toggled.connect(lambda: update_algorithm("AES"))
    
    chacha_radio = QRadioButton("ChaCha20")
    chacha_radio.setChecked(current_algorithm == "ChaCha20")
    chacha_radio.toggled.connect(lambda: update_algorithm("ChaCha20"))
    
    fernet_radio = QRadioButton("Fernet")
    fernet_radio.setChecked(current_algorithm == "Fernet")
    fernet_radio.toggled.connect(lambda: update_algorithm("Fernet"))
    
    radio_layout = QHBoxLayout()
    radio_layout.addWidget(aes_radio)
    radio_layout.addWidget(chacha_radio)
    radio_layout.addWidget(fernet_radio)
    vbox.addLayout(radio_layout)

    file_label = QLabel("📁 No encrypted image selected")
    select_btn = create_button(
        "Select Encrypted Image", 
        "assets/folder.svg", 
        lambda: select_encrypted_image_for_decryption(file_label)
    )

    decrypt_btn = create_button(
        "Decrypt Image", 
        "assets/decrypt.svg", 
        lambda: decrypt_image_ui(window),
        icon_size=24,
        button_style="""
            QPushButton {
                background-color: #3498DB;
                color: white;
                font-size: 17px;
                font-weight: bold;
                border-radius: 14px;
                padding: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """
    )

    btn_back = create_button(
        "Back", 
        "assets/back.svg", 
        lambda: (window.close(), parent_window.show() if parent_window else None),
        icon_size=24,
        button_style="""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                font-size: 15px;
                font-weight: 600;
                border-radius: 14px;
                padding: 10px 20px;
                border: none;
            }
            QPushButton:hover {
                background-color: #FF6B6B;
            }
        """
    )
    btn_back.setFixedHeight(42)

    vbox.addWidget(select_btn)
    vbox.addWidget(file_label)
    vbox.addWidget(decrypt_btn)
    vbox.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
    vbox.addWidget(btn_back, alignment=Qt.AlignRight)

    layout.addWidget(card)
    window.show()

    if parent_window:
        parent_window.hide()

def update_algorithm(selected_algorithm):
    global current_algorithm
    current_algorithm = selected_algorithm
    

