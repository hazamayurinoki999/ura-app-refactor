# gui/main_window.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSpinBox, QScrollArea
)
from gui.canvas_widget import CanvasWidget
from config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        layout = QVBoxLayout(self)

        # タイトル入力欄
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("タイトルを入力（任意）")
        layout.addWidget(self.title_input)

        # 線分図の本数
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("線分図の本数："))
        self.count_spin = QSpinBox()
        self.count_spin.setMinimum(1)
        self.count_spin.setValue(1)
        control_layout.addWidget(self.count_spin)
        layout.addLayout(control_layout)

        # 「線分図を生成」ボタン
        self.generate_btn = QPushButton("線分図を生成")
        layout.addWidget(self.generate_btn)

        # キャンバス（スクロール付き）
        self.canvas = CanvasWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.canvas)
        layout.addWidget(scroll, 1)
