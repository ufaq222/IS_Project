# utils.py

from PyQt5.QtWidgets import QApplication

def center_window(window, width, height):
    screen = QApplication.primaryScreen()
    screen_geometry = screen.availableGeometry()
    x = (screen_geometry.width() - width) // 2
    y = (screen_geometry.height() - height) // 2
    window.setGeometry(x, y, width, height)
