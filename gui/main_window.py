from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QScrollArea, QGroupBox, QGridLayout
)
from gui.canvas_widget import CanvasWidget
from config import APP_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_TITLE)
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        main_layout = QVBoxLayout(self)

        # === 設定パネル ===
        setting_box = QGroupBox("設定パネル")
        setting_layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("タイトルを入力（任意）")
        setting_layout.addWidget(self.title_input)

        spin_layout = QHBoxLayout()
        spin_layout.addWidget(QLabel("線分図の本数："))
        self.count_spin = QSpinBox()
        self.count_spin.setMinimum(1)
        self.count_spin.setValue(1)
        spin_layout.addWidget(self.count_spin)
        setting_layout.addLayout(spin_layout)

        self.generate_btn = QPushButton("線分図を生成")
        setting_layout.addWidget(self.generate_btn)

        setting_box.setLayout(setting_layout)
        main_layout.addWidget(setting_box)

        # === 入力パネル ===
        input_box = QGroupBox("入力フォーム")
        input_layout = QVBoxLayout()
        self.input_grid = QVBoxLayout()
        input_layout.addLayout(self.input_grid)
        input_box.setLayout(input_layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(input_box)
        main_layout.addWidget(scroll, 2)

        # === 描画キャンバス ===
        self.canvas = CanvasWidget()
        canvas_scroll = QScrollArea()
        canvas_scroll.setWidgetResizable(True)
        canvas_scroll.setWidget(self.canvas)
        main_layout.addWidget(canvas_scroll, 3)

        # 各種初期化
        self.segment_boxes = []
        self.edits = []
        self._rebuild_inputs()

        # イベント接続
        self.count_spin.valueChanged.connect(self._rebuild_inputs)
        self.generate_btn.clicked.connect(lambda: print("生成ボタン押されました"))

    def _rebuild_inputs(self):
        prev_segs = [sb.value() for sb in self.segment_boxes]
        prev_left = [edit[0].text() for edit in self.edits]
        prev_tops = [[t.text() for t in edit[1]] for edit in self.edits]
        prev_rats = [[r.text() for r in edit[2]] for edit in self.edits]

        while self.input_grid.count():
            item = self.input_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                while item.layout().count():
                    sub = item.layout().takeAt(0)
                    if sub.widget():
                        sub.widget().deleteLater()

        self.segment_boxes.clear()
        self.edits.clear()

        row_count = self.count_spin.value()

        for i in range(row_count):
            outer_layout = QGridLayout()

            # ラベル行
            left_label = QLineEdit()
            left_label.setPlaceholderText(f"ラベル{i+1}")
            if i < len(prev_left):
                left_label.setText(prev_left[i])
            outer_layout.addWidget(left_label, 0, 0, 1, 1)

            seg_spin = QSpinBox()
            seg_spin.setMinimum(1)
            default_val = prev_segs[i] if i < len(prev_segs) else 2
            seg_spin.setValue(default_val)
            outer_layout.addWidget(seg_spin, 1, 0, 1, 1)

            tops = []
            rats = []

            for j in range(seg_spin.value()):
                top = QLineEdit()
                top.setPlaceholderText(f"上ラベル{j+1}")
                if i < len(prev_tops) and j < len(prev_tops[i]):
                    top.setText(prev_tops[i][j])
                outer_layout.addWidget(top, 1, j + 1)
                tops.append(top)

                rat = QLineEdit()
                rat.setPlaceholderText(f"比{j+1}")
                if i < len(prev_rats) and j < len(prev_rats[i]):
                    rat.setText(prev_rats[i][j])
                outer_layout.addWidget(rat, 2, j + 1)
                rats.append(rat)

            container = QWidget()
            container.setLayout(outer_layout)
            self.input_grid.addWidget(container)
            self.segment_boxes.append(seg_spin)
            self.edits.append((left_label, tops, rats))

            seg_spin.valueChanged.connect(self._rebuild_inputs)
