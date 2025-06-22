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
        # 入力フォームの配置場所（グリッド）
        self.input_grid = QVBoxLayout()
        layout.addLayout(self.input_grid)

        # 行ごとの SpinBox と 入力欄を管理するリスト
        self.segment_boxes = []
        self.edits = []

        # 最初のフォーム作成
        self._rebuild_inputs()

        # 行数変更時にフォームを再生成
        self.count_spin.valueChanged.connect(self._rebuild_inputs)

        # ボタン押下時の処理（仮）
        self.generate_btn.clicked.connect(lambda: print("生成ボタン押されました"))

    def _rebuild_inputs(self):
        # 既存の入力欄をすべて削除
        while self.input_grid.count():
            item = self.input_grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        self.segment_boxes.clear()
        self.edits.clear()

        row_count = self.count_spin.value()

        for i in range(row_count):
            row_layout = QHBoxLayout()

            # 左ラベル
            left_label = QLineEdit()
            left_label.setPlaceholderText(f"ラベル{i+1}")
            row_layout.addWidget(left_label)

            # 分割数SpinBox（仮：2固定）
            seg_spin = QSpinBox()
            seg_spin.setMinimum(1)
            seg_spin.setValue(2)
            row_layout.addWidget(seg_spin)

            # 比率入力欄（仮に2つ）
            rats = []
            tops = []
            for j in range(2):
                top = QLineEdit()
                top.setPlaceholderText(f"上ラベル{j+1}")
                rat = QLineEdit()
                rat.setPlaceholderText(f"比{j+1}")
                row_layout.addWidget(top)
                row_layout.addWidget(rat)
                tops.append(top)
                rats.append(rat)

            self.input_grid.addLayout(row_layout)
            self.segment_boxes.append(seg_spin)
            self.edits.append((left_label, tops, rats))
