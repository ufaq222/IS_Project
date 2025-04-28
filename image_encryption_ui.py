from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QFileDialog, QMessageBox,
    QVBoxLayout, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy,
    QComboBox, QLineEdit, QRadioButton, QInputDialog
)
from PyQt5.QtGui import QIcon, QFont, QColor, QPainter
from PyQt5.QtCore import Qt, QSize
import image  # This imports our encryption functions
from PyQt5.QtGui import QMovie

encrypt_image_path = None
image_path = None
current_algorithm = "AES"  # Default algorithm

def select_file(label, dialog_type='open', file_type='Images (*.png *.jpg *.jpeg)', is_save=False):
    global image_path, encrypt_image_path
    dialog_func = QFileDialog.getSaveFileName if is_save else QFileDialog.getOpenFileName

    if is_save:
        file_type = 'Encrypted Image Files (*.enc)'

    path, _ = dialog_func(None, "Select Image" if not is_save else "Save Encrypted File As", "", file_type)
    if path:
        if is_save:
            if not path.endswith(".enc"):
                path += ".enc"
            encrypt_image_path = path
            label.setText(f"💾 {encrypt_image_path.split('/')[-1]}")
        else:
            image_path = path
            label.setText(f"📁 {image_path.split('/')[-1]}")

def encrypt(parent=None):
    global current_algorithm
    if not image_path or not encrypt_image_path:
        QMessageBox.warning(parent, "Missing Info", "⚠ Please select both input image and save path.")
        return
    
    password, ok = QInputDialog.getText(parent, 'Password', 'Enter encryption password:', QLineEdit.Password)
    if not ok or len(password) < 6:
        QMessageBox.warning(parent, "Weak Password", "⚠ Password must be at least 6 characters long.")
        return
    
    try:
        if current_algorithm == "AES":
            image.encrypt_image_aes(image_path, encrypt_image_path, password)
        elif current_algorithm == "ChaCha20":
            image.encrypt_image_chacha20(image_path, encrypt_image_path, password)
        elif current_algorithm == "Fernet":
            image.encrypt_image_fernet(image_path, encrypt_image_path, password)
            
        QMessageBox.information(parent, "Success", "✅ Image encrypted successfully!")
    except Exception as e:
        QMessageBox.critical(parent, "Error", f"❌ Encryption failed: {e}")

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

def create_algorithm_selection():
    algo_frame = QFrame()
    algo_layout = QHBoxLayout()  # Change from QVBoxLayout to QHBoxLayout

    aes_radio = QRadioButton("AES")
    chacha_radio = QRadioButton("ChaCha20")
    fernet_radio = QRadioButton("Fernet")
    
    aes_radio.setChecked(True)  # Default selection

    aes_radio.toggled.connect(lambda: set_algorithm("AES"))
    chacha_radio.toggled.connect(lambda: set_algorithm("ChaCha20"))
    fernet_radio.toggled.connect(lambda: set_algorithm("Fernet"))
    
    # Add radio buttons to the layout
    algo_layout.addWidget(aes_radio)
    algo_layout.addWidget(chacha_radio)
    algo_layout.addWidget(fernet_radio)

    algo_frame.setLayout(algo_layout)
    
    # Apply consistent background color for radio buttons
    for radio_button in [aes_radio, chacha_radio, fernet_radio]:
        radio_button.setStyleSheet("""
            QRadioButton {
                background-color: #34495E;
                color: white;
                border-radius: 8px;
                padding: 5px;
            }
            QRadioButton:hover {
                background-color: #3E5871;
            }
        """)

    return algo_frame

def set_algorithm(algorithm_name):
    global current_algorithm
    current_algorithm = algorithm_name

def run_encryption_ui(parent_window=None):
    global current_algorithm
    
    window = QWidget()
    window.setWindowTitle("🔐 Image Encryption")
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
    """)
    window.setFixedSize(640, 750)

    layout = QVBoxLayout(window)
    layout.setContentsMargins(30, 30, 30, 30)
    layout.setSpacing(25)

    title = QLabel("🔒 Secure Your Image")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 26px; font-weight: bold; color: #1ABC9C; letter-spacing: 1px;")
    layout.addWidget(title)
    
    gif_label = QLabel()
    gif_label.setAlignment(Qt.AlignCenter)
    gif = QMovie("assets/image_encryption.gif")
    gif.setScaledSize(QSize(250, 200))
    gif_label.setMovie(gif)
    gif.start()
    layout.addWidget(gif_label)

    # Create the main card
    card = GlassFrame()
    vbox = QVBoxLayout(card)
    vbox.setSpacing(20)

    # Create the algorithm selection frame
    algo_selection_frame = create_algorithm_selection()
    vbox.addWidget(algo_selection_frame)

    # Image selection and encryption buttons
    image_label = QLabel("📷 No image selected.")
    btn_select_image = create_button("Choose Image", "assets/folder.svg", lambda: select_file(image_label))

    encrypted_label = QLabel("💾 No save path selected.")
    btn_save_path = create_button("Set Save Path", "assets/folder.svg", lambda: select_file(encrypted_label, is_save=True))

    btn_encrypt = create_button("Encrypt Now", "assets/encrypt.svg", lambda: encrypt(window), icon_size=24, button_style=""" 
        QPushButton {
            background-color: #27AE60;
            color: white;
            font-size: 17px;
            font-weight: bold;
            border-radius: 14px;
            padding: 8px;
            border: none;
        }
        QPushButton:hover {
            background-color: #2ECC71;
        }
    """)

    btn_back = create_button("Back", "assets/back.svg", lambda: (window.close(), parent_window.show() if parent_window else None), icon_size=24, button_style=""" 
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
    """)
    btn_back.setFixedHeight(42)

    # Add widgets to the layout
    vbox.addWidget(btn_select_image)
    vbox.addWidget(image_label)
    vbox.addWidget(btn_save_path)
    vbox.addWidget(encrypted_label)
    vbox.addWidget(btn_encrypt)
    vbox.addSpacerItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))
    vbox.addWidget(btn_back, alignment=Qt.AlignRight)

    layout.addWidget(card)
    window.show()

    if parent_window:
        parent_window.hide()
