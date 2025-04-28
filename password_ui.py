import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QListWidget, QProgressBar, QMessageBox,
    QGroupBox, QCheckBox, QWidget,QTextEdit,QAction,QGraphicsOpacityEffect
)
from PyQt5.QtGui import QFont,QMovie
from PyQt5.QtCore import Qt,QSize
from password_strength import PasswordAnalyzer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtWidgets import QDesktopWidget

class ToggleSwitch(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self._checked = False
        self._circle_position = 3
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setDuration(200)

    def mousePressEvent(self, event):
        self._checked = not self._checked
        self.toggle_animation()
        self.parent().toggle_mode()  # Calls the theme switch in main window

    def toggle_animation(self):
        start = 3 if not self._checked else self.width() - 27
        end = self.width() - 27 if not self._checked else 3
        self.animation.setStartValue(start)
        self.animation.setEndValue(end)
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # Background
        bg_color = QColor("#00c853") if self._checked else QColor("#ccc")
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 15, 15)
        # Circle
        painter.setBrush(Qt.white)
        painter.drawEllipse(QRect(int(self._circle_position), 3, 24, 24))

    def get_circle_position(self):
        return self._circle_position

    def set_circle_position(self, pos):
        self._circle_position = pos
        self.update()

    circle_position = pyqtProperty(float, get_circle_position, set_circle_position)



from PyQt5.QtGui import QFont, QMovie, QIcon
from PyQt5.QtCore import Qt, QSize


class PwnedPasswordUI(QWidget):
    def __init__(self, parent_window=None):
        super().__init__()
        self.setWindowTitle("Pwned Passwords")
        self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet("background-color: black; color: white;")

        self.analyzer = PasswordAnalyzer()
        self.parent_window = parent_window
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 30, 40, 20)  # Padding from left and right
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        # === Title Label ===
        label = QLabel("';--have i been pwned?")
        label.setStyleSheet("""
            QLabel {
                font-size: 38px;
                font-weight: bold;
                color: #00FFFF;
                padding: 12px;
                border-radius: 10px;
                background-color: #2F2F2F;
                text-align: center;
            }
        """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # === Subtitle Label ===
        password_label = QLabel("Check if your password is in a data breach")
        password_label.setFont(QFont("Arial", 12))
        password_label.setStyleSheet("color: #AAAAAA;")
        password_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(password_label)
        layout.addSpacing(20)
        # === GIF Animation (placed under the label now) ===
        gif_label = QLabel()
        gif_movie = QMovie("assets/password.gif")
        gif_movie.setScaledSize(QSize(350, 150))
        gif_label.setMovie(gif_movie)
        gif_movie.start()
        layout.addWidget(gif_label, alignment=Qt.AlignCenter)

        layout.addStretch(1)

        # === Input and Button ===
        input_layout = QHBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter your password")
        self.input_field.setEchoMode(QLineEdit.Password)
        self.input_field.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #00FFFF;
                border-radius: 8px;
                font-size: 18px;
                background-color: #121212;
                color: #00FFFF;
            }
        """)
        # === Toggle Password Visibility Icon ===
        self.toggle_action = QAction(QIcon("assets/eye-show.svg"), "", self.input_field)
        self.toggle_action.triggered.connect(self.toggle_password_visibility)
        self.input_field.addAction(self.toggle_action, QLineEdit.TrailingPosition)

        self.check_button = QPushButton("pwned?")
        self.check_button.setCursor(Qt.PointingHandCursor)
        self.check_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00FFFF, stop:1 #006666
                );
                color: black;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:0,
                    stop:0 #33FFFF, stop:1 #009999
                );
            }
        """)
        self.check_button.clicked.connect(self.check_password)

        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.check_button)

        layout.addLayout(input_layout)

        # === Result Area ===
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.result_area.setGraphicsEffect(QGraphicsOpacityEffect(self.result_area))
        self.result_area.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: white;
                border: none;
                font-size: 16px;
                padding: 10px;
            }
        """)
        self.result_area.setVisible(False)
        layout.addWidget(self.result_area)

        layout.addStretch(2)

        # === Back Button ===
        self.back_button = QPushButton("  Back")
        self.back_button.setFixedHeight(40)
        self.back_button.setIcon(QIcon("assets/back.png"))  # Use your icon path here
        self.back_button.setIconSize(QSize(20, 20))
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #B22222;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #FF0000;
            }
        """)
        self.back_button.clicked.connect(self.handle_back)
        layout.addSpacing(15)
        layout.addWidget(self.back_button, alignment=Qt.AlignHCenter)

        self.setLayout(layout)

    def toggle_password_visibility(self):
        if self.input_field.echoMode() == QLineEdit.Password:
            self.input_field.setEchoMode(QLineEdit.Normal)
            self.toggle_action.setIcon(QIcon("assets/eye-hide.svg"))
        else:
            self.input_field.setEchoMode(QLineEdit.Password)
            self.toggle_action.setIcon(QIcon("assets/eye-show.svg"))
            
    def check_password(self):
        password = self.input_field.text()
        if not password:
            self.show_result("❌ Please enter a password.", "#8B0000")
            return
        if len(password) < 6:
            self.show_result("❌ Password must be at least 6 characters long.", "#8B0000")
            return

        is_pwned, message = self.analyzer.is_password_pwned(password)
        if is_pwned:
            self.show_result(
                f"<b>Oh no — pwned!</b>\n{message}\n\n"
                "This password has previously appeared in a data breach and should never be used.",
                "#8B0000"
            )
        else:
            self.show_result(
                "<b>Good news — no pwnage found!</b>\n"
                "This password wasn't found in any of the Pwned Passwords loaded into Have I Been Pwned.",
                "#0b6623"
            )

    def show_result(self, text, bg_color):
        self.result_area.setStyleSheet(f"""
            QTextEdit {{
                background-color: {bg_color};
                color: white;
                border: none;
                font-size: 16px;
                padding: 10px;
            }}
        """)
        self.result_area.setText(text)
        self.result_area.setVisible(True)

        effect = self.result_area.graphicsEffect()
        self.fade = QPropertyAnimation(effect, b"opacity")
        self.fade.setDuration(600)
        self.fade.setStartValue(0)
        self.fade.setEndValue(1)
        self.fade.start()

    def handle_back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()


class PasswordUI(QWidget):
    def __init__(self,parent_window=None):
        super().__init__()
        self.analyzer = PasswordAnalyzer()
        self.parent_window = parent_window
        self.dark_mode = True  # Start in dark mode
        self.dark_mode_styles = {
            "background": "#000000",
            "text": "white",
            "highlight": "#00FFFF",
            "button": "#00b894",
            "group_border": "#00FFFF",
        }
        self.light_mode_styles = {
            "background": "#f0f0f0",
            "text": "black",
            "highlight": "#006080",
            "button": "#00796b",
            "group_border": "#00796b",
}

        self.setWindowTitle("🔐 Password Analyzer")
        self.setFixedSize(700,700)
        self.setStyleSheet("background-color: #000000; color: white;")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        # === Title ===
        self.title = QLabel("Password Strength Checker")
        self.title.setFont(QFont("Arial", 20, QFont.Bold))
        self.title.setStyleSheet("color: #00FFFF;")
        self.title.setAlignment(Qt.AlignCenter)

        # === How Secure is Your Password? ===
        self.security_label = QLabel("How Secure is Your Password?")
        self.security_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.security_label.setStyleSheet("color: #ffffff; background-color: #333333; padding: 10px; border-radius: 5px;")
        self.security_label.setAlignment(Qt.AlignCenter)

        # === Instructions + Checkbox ===
        instructions_layout = QVBoxLayout()
        self.instruction1 = QLabel("Take the Password Test")
        self.instruction1.setFont(QFont("Arial", 14, QFont.Bold))
        self.instruction1.setStyleSheet("color: white;")

        self.instruction2 = QLabel("Tip: Stronger passwords use different types of characters")
        self.instruction2.setFont(QFont("Arial", 11))
        self.instruction2.setStyleSheet("color: #bbbbbb;")

        self.show_password_checkbox = QCheckBox("Show password")
        self.show_password_checkbox.setStyleSheet("color: #dddddd;")
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        instructions_layout.addWidget(self.instruction1)
        instructions_layout.addWidget(self.instruction2)
        instructions_layout.addWidget(self.show_password_checkbox)

        # === Password Input Group ===
        self.input_group = QGroupBox("Enter Your Password")
        self.input_group.setStyleSheet("""
            QGroupBox {
                color: #00FFFF;
                font-size: 16px;
                border: 2px solid #00FFFF;
                border-radius: 10px;
                margin-top: 10px;
            }
            QGroupBox:title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        input_layout = QVBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter your password here")
        self.input_field.setEchoMode(QLineEdit.Password)
        self.input_field.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 8px; max-width: 400px")
        self.input_field.textChanged.connect(self.update_analysis)

        input_layout.addWidget(self.input_field)
        self.input_group.setLayout(input_layout)

        # === Password Analysis Components ===
        self.strength_bar = QProgressBar()
        self.strength_bar.setMaximum(100)
        self.strength_bar.setTextVisible(False)
        self.strength_bar.setStyleSheet("height: 20px; border-radius: 10px;")
        
        self.strength_description_label = QLabel("")
        self.strength_description_label.setFont(QFont("Arial", 12))
        self.strength_description_label.setAlignment(Qt.AlignCenter)
        self.strength_description_label.setStyleSheet("color: white;")

        # self.strength_label = QLabel("Strength: ")
        # self.time_label = QLabel("Time to Crack: ")
        # self.entropy_label = QLabel("Entropy: ")

        self.rules_list = QListWidget()
        self.rules_list.setStyleSheet("font-size: 14px; background: #2a2a3d; border: none;")

        self.generate_button = QPushButton("Generate Strong Password")
        self.generate_button.setStyleSheet("padding: 10px; background: #00b894; color: white; font-weight: bold; border-radius: 8px;")
        self.generate_button.clicked.connect(self.generate_password)

        # === Character Type Indicators ===
        self.char_types_layout = QHBoxLayout()
        self.char_title_label = QLabel("0 characters containing:")
        self.char_title_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.char_title_label.setStyleSheet("color: #aaaaaa;")
        self.char_types_layout.addWidget(self.char_title_label)

        self.lowercase_label = self.create_colored_type_label("Lower case")
        self.uppercase_label = self.create_colored_type_label("Upper case")
        self.numbers_label = self.create_colored_type_label("Numbers")
        self.symbols_label = self.create_colored_type_label("Symbols")

        for label in [self.lowercase_label, self.uppercase_label, self.numbers_label, self.symbols_label]:
            self.char_types_layout.addWidget(label)

        # === Add Character Type row below the password input group ===
        char_types_widget = QWidget()
        char_types_widget.setLayout(self.char_types_layout)

        # === Time to Crack Labels ===
        self.time_to_crack_label = QLabel("Time to Crack your password:")
        self.time_to_crack_label.setFont(QFont("Arial", 10))
        self.time_to_crack_label.setAlignment(Qt.AlignCenter)
        self.time_to_crack_label.setStyleSheet("color: #ffffff;")

        # === 0 Seconds Label ===
        self.crack_time_value_label = QLabel("0 seconds")
        self.crack_time_value_label.setFont(QFont("Arial", 12))
        self.crack_time_value_label.setAlignment(Qt.AlignCenter)
        self.crack_time_value_label.setStyleSheet("color: #ffffff;")
        
                # === Review Label ===
        self.review_label = QLabel("")
        self.review_label.setFont(QFont("Arial", 10))
        self.review_label.setAlignment(Qt.AlignCenter)
        self.review_label.setStyleSheet("color: #ffffff;")
        
        # self.toggle_mode_button = QPushButton("Switch to Light Mode")
        # self.toggle_mode_button.setStyleSheet("padding: 5px; font-weight: bold;")
        # self.toggle_mode_button.clicked.connect(self.toggle_mode)
        # layout.addWidget(self.toggle_mode_button)
        
        top_bar = QHBoxLayout()
        top_bar.addStretch()  # Pushes toggle button to the right

        self.toggle_mode_button = ToggleSwitch(self)
        top_bar.addWidget(self.toggle_mode_button)
        layout.addLayout(top_bar)  # ✅ Add top bar layout instead of direct widget
       
                # === Back Button ===
        self.back_button = QPushButton("Back")
        self.back_button.setFixedSize(100, 40)
        self.back_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #34495e;
                color: white;
                font-weight: bold;
                border-radius: 8px;
            }
        """)
        self.back_button.clicked.connect(self.back)  # Connect to your back function

        # === Pwned Button ===
        self.pwned_button = QPushButton("Pwned")
        self.pwned_button.setFixedSize(100, 40)
        self.pwned_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                background: #e74c3c;
                color: white;
                font-weight: bold;
                border-radius: 8px;
            }
        """)
        self.pwned_button.clicked.connect(self.open_pwned_window)

        # === Horizontal Layout for Buttons ===
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)    # Left-aligned
        button_layout.addStretch()                   # Spacer in the middle
        button_layout.addWidget(self.pwned_button)   # Right-aligned
        # Use a QVBoxLayout to stack the labels vertically
        time_layout = QVBoxLayout()
        time_layout.addWidget(self.time_to_crack_label)
        time_layout.addWidget(self.crack_time_value_label)

        # === Main Layout ===
        layout.addWidget(self.title)
        layout.addWidget(self.security_label)  # <-- Add this label
        layout.addLayout(instructions_layout)  # Instructions
        layout.addWidget(self.input_group)          # Password Input
        layout.addWidget(char_types_widget)  # Add the character type row below the input field
        layout.addLayout(time_layout)        # Add the "Time to Crack" labels in the center
        layout.addWidget(self.review_label)  # Add this line
        layout.addWidget(self.strength_bar)
        layout.addWidget(self.strength_description_label)
        # layout.addWidget(self.strength_label)
        # layout.addWidget(self.time_label)
        # layout.addWidget(self.entropy_label)
        layout.addWidget(QLabel("Password Requirements:"))
        layout.addWidget(self.rules_list)
        layout.addWidget(self.generate_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        
        # Center the window on the screen
        self.center_window()
        self.apply_styles(self.dark_mode_styles)
    
    def back(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()
        
    def open_pwned_window(self):
        # Create the PwnedWindow
        self.pwned_window = PwnedPasswordUI(parent_window=self)

        # Get the screen geometry (monitor size)
        screen_geometry = QDesktopWidget().availableGeometry()

        # Calculate the center position
        center_x = (screen_geometry.width() - self.pwned_window.width()) // 2
        center_y = (screen_geometry.height() - self.pwned_window.height()) // 2

        # Move the window to the center of the screen
        self.pwned_window.move(center_x, center_y)

        # Close the current window
        self.hide()

        # Show the PwnedWindow
        self.pwned_window.show()
    def toggle_mode(self):
        self.dark_mode = not self.dark_mode
        new_mode = self.light_mode_styles if not self.dark_mode else self.dark_mode_styles
        self.apply_styles(new_mode)
    
    def apply_styles(self, style=None):
        # Define light mode color scheme
        style = style or {
            'background': '#F5F7FA',  # Soft off-white
            'text': '#2D3436',        # Dark gray
            'button': '#0984E3',      # Vibrant blue
            'highlight': '#00B894',   # Teal green
            'group_border': '#DDE1E6', # Light gray
        }

        # Apply styles to the main widget
        self.setStyleSheet(f"background-color: {style['background']}; color: {style['text']};")

        self.title.setStyleSheet(f"color: {'#301934' if not self.dark_mode else '#00FFFF'};")
        self.instruction1.setStyleSheet(f"color: {'#2D3436' if not self.dark_mode else '#FFFFFF'};")
        self.instruction2.setStyleSheet(f"color: {'#636E72' if not self.dark_mode else '#bbbbbb'};")

        # Input field
        self.input_field.setStyleSheet(f"padding: 10px; font-size: 16px; border-radius: 8px; color: {style['text']}; background: {'#ffffff' if not self.dark_mode else '#2a2a3d'};")

        # Generate button
        self.generate_button.setStyleSheet(f"padding: 10px; background: {style['button']}; color: white; font-weight: bold; border-radius: 8px;")

        # Show password checkbox
        self.show_password_checkbox.setStyleSheet(f"color: {style['text']};")

        # Strength bar
        self.strength_bar.setStyleSheet("height: 20px; border-radius: 10px;")

        # Rules list
        self.rules_list.setStyleSheet(f"font-size: 14px; background: {'#ffffff' if not self.dark_mode else '#2a2a3d'}; color: {style['text']}; border: none;")

        # Labels
        self.review_label.setStyleSheet(f"color: {style['text']};")
        self.time_to_crack_label.setStyleSheet(f"color: {style['text']};")
        self.crack_time_value_label.setStyleSheet(f"color: {style['text']};")
        self.char_title_label.setStyleSheet(f"color: {style['text']};")

        # Input group box
        self.input_group.setStyleSheet(f"""
            QGroupBox {{
                color: {style['highlight']};
                font-size: 16px;
                border: 2px solid {style['group_border']};
                border-radius: 10px;
                margin-top: 10px;
            }}
            QGroupBox:title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }}
        """)

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.input_field.setEchoMode(QLineEdit.Normal)
        else:
            self.input_field.setEchoMode(QLineEdit.Password)

    

    def update_analysis(self):
        password = self.input_field.text()

        if not password:  # Check if the password is empty
            self.strength_description_label.setText("")  # No text for empty password
            self.strength_bar.setValue(0)
            self.strength_bar.setStyleSheet("QProgressBar::chunk {background: #7f8c8d; border-radius: 10px;}")

            # Reset character types and time-to-crack label
            self.update_char_types(password)
            self.char_title_label.setText("0 characters containing:")
            self.crack_time_value_label.setText("0 seconds")
            self.review_label.setText("")
            
            # Clear requirements list content
            self.rules_list.clear()

            # You can choose to hide the progress bar if desired, or leave it visible as you did before
            self.strength_bar.setVisible(False)
            return

        result = self.analyzer.analyze_password(password)

        strength = result['strength']
        self.strength_description_label.setText(f"Strength: {strength}")  # Only show strength

        # Set color based on strength
        self.strength_description_label.setStyleSheet(self.get_strength_color(strength))  # Apply color styling
        
        self.char_title_label.setText(f"{result['total_characters']} characters containing:")
        
        # Clear and update requirements list
        self.rules_list.clear()  # Clear previous items
        for key, value in result['requirements'].items():
            status = '✔️' if value else '❌'
            label = key.capitalize()
            self.rules_list.addItem(f"{status} {label}")
        self.strength_bar.setVisible(True)  # Show progress bar

        
        bar_value = {
            "Very Weak": 10,
            "Weak": 30,
            "Moderate": 50,
            "Strong": 75,
            "Very Strong": 100
        }.get(strength, 0)

        self.strength_bar.setValue(bar_value)
        bar_color = self.get_bar_color(strength)
        self.strength_bar.setStyleSheet(f"QProgressBar::chunk {{background: {bar_color}; border-radius: 10px;}}")

        # Update character types
        self.update_char_types(password)

        # Update the time-to-crack label dynamically
        self.crack_time_value_label.setText(result['time_to_crack'])

        # Update the review label with feedback
        self.review_label.setText(result['review'])
        


    def get_strength_color(self, strength):
        # Return the color based on the strength level
        return {
            "Very Weak": "color: #e74c3c;",  # Red
            "Weak": "color: #e67e22;",       # Orange
            "Moderate": "color: #f1c40f;",   # Yellow
            "Strong": "color: #2ecc71;",     # Green
            "Very Strong": "color: #00cec9;" # Cyan
        }.get(strength, "color: #7f8c8d;")  # Default color


    def get_bar_color(self, strength):
        return {
            "Very Weak": "#e74c3c",
            "Weak": "#e67e22",
            "Moderate": "#f1c40f",
            "Strong": "#2ecc71",
            "Very Strong": "#00cec9"
        }.get(strength, "#7f8c8d")

    def create_colored_type_label(self, text):
        label = QLabel(text)
        label.setFont(QFont("Arial", 11))
        label.setStyleSheet("color: #aaaaaa;")
        return label

    def update_char_types(self, password):
        # Reset colors
        self.lowercase_label.setStyleSheet("color: #aaaaaa;")
        self.uppercase_label.setStyleSheet("color: #aaaaaa;")
        self.numbers_label.setStyleSheet("color: #aaaaaa;")
        self.symbols_label.setStyleSheet("color: #aaaaaa;")

        # Check password content
        if any(c.islower() for c in password):
            self.lowercase_label.setStyleSheet("color: #00b894;")
        if any(c.isupper() for c in password):
            self.uppercase_label.setStyleSheet("color: #00b894;")
        if any(c.isdigit() for c in password):
            self.numbers_label.setStyleSheet("color: #00b894;")
        if any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in password):
            self.symbols_label.setStyleSheet("color: #00b894;")

    def generate_password(self):
        password = self.analyzer.generate_password()
        self.input_field.setText(password)
        QMessageBox.information(self, "Generated Password", f"A strong password has been generated:\n\n{password}")


    def center_window(self):
        # Center the window on the screen
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = self.frameGeometry()
        center_position = screen_geometry.center() - window_geometry.center()
        self.move(center_position)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = PasswordUI()
    ui.show()
    sys.exit(app.exec_())
