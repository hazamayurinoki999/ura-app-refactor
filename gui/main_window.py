# gui/main_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("動作確認用メインウィンドウ"))
