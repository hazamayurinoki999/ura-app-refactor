from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSpinBox, QScrollArea, QGroupBox, QGridLayout, QTextEdit
)
from PyQt5.QtGui import QTextOption
from PyQt5.QtCore import Qt
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

        self.fit_btn = QPushButton("フィッティング")
        setting_layout.addWidget(self.fit_btn)

        # 合計モード切替ボタン（→ キャンセルボタンと交互表示）
        sum_layout = QHBoxLayout()
        self.sum_btn = QPushButton("合計")
        self.cancel_sum_btn = QPushButton("×")
        self.cancel_sum_btn.setFixedWidth(30)
        self.cancel_sum_btn.hide()  # 初期は非表示
        sum_layout.addWidget(self.sum_btn)
        sum_layout.addWidget(self.cancel_sum_btn)
        setting_layout.addLayout(sum_layout)

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
        self.generate_btn.clicked.connect(self._handle_generate)
        self.fit_btn.clicked.connect(self._handle_fit)
        self.sum_btn.clicked.connect(self._handle_sum_mode_on)
        self.cancel_sum_btn.clicked.connect(self._handle_sum_mode_off)

    def _rebuild_inputs(self):
        prev_segs = [sb.value() for sb in self.segment_boxes]
        prev_left = [edit[0].text() for edit in self.edits]
        prev_tops = [[t.text() for t in edit[1]] for edit in self.edits]
        prev_rats = [[r.text() for r in edit[2]] for edit in self.edits]
        prev_uppers = [[u.toPlainText() for u in edit[3]] if len(edit) > 3 else [] for edit in self.edits]

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

            left_label = QLineEdit()
            left_label.setPlaceholderText(f"ラベル{i+1}")
            left_label.setMaxLength(20)
            if i < len(prev_left):
                left_label.setText(prev_left[i])
            outer_layout.addWidget(left_label, 0, 0, 1, -1)

            seg_spin = QSpinBox()
            seg_spin.setMinimum(1)
            default_val = prev_segs[i] if i < len(prev_segs) else 2
            seg_spin.setValue(default_val)
            outer_layout.addWidget(seg_spin, 1, 0)

            uppers = []
            tops = []
            rats = []

            for j in range(seg_spin.value()):
                upper = QTextEdit()
                upper.setPlaceholderText(f"上ラベル{j+1}")
                upper.setAcceptRichText(False)
                upper.setMaximumHeight(40)
                upper.setWordWrapMode(QTextOption.WrapAtWordBoundaryOrAnywhere)
                if i < len(prev_uppers) and j < len(prev_uppers[i]):
                    upper.setPlainText(prev_uppers[i][j])
                outer_layout.addWidget(upper, 1, j + 1)
                uppers.append(upper)

                top = QLineEdit()
                top.setPlaceholderText(f"値{j+1}")
                top.setMaxLength(10)
                if i < len(prev_tops) and j < len(prev_tops[i]):
                    top.setText(prev_tops[i][j])
                outer_layout.addWidget(top, 2, j + 1)
                tops.append(top)

                rat = QLineEdit()
                rat.setPlaceholderText(f"比{j+1}")
                rat.setMaxLength(10)
                if i < len(prev_rats) and j < len(prev_rats[i]):
                    rat.setText(prev_rats[i][j])
                outer_layout.addWidget(rat, 3, j + 1)
                rats.append(rat)

            container = QWidget()
            container.setLayout(outer_layout)
            self.input_grid.addWidget(container)
            self.segment_boxes.append(seg_spin)
            self.edits.append((left_label, tops, rats, uppers))

            seg_spin.valueChanged.connect(self._rebuild_inputs)

    def _gather_input_data(self):
        data = []
        for edit in self.edits:
            label_edit, value_edits, ratio_edits, upper_edits = edit
            label = label_edit.text()
            values = [v.text() for v in value_edits]
            ratios = [r.text() for r in ratio_edits]
            uppers = [u.toPlainText() for u in upper_edits]
            data.append({
                'label': label,
                'values': values,
                'ratios': ratios,
                'uppers': uppers
            })
        return data

    def _handle_generate(self):
        data = self._gather_input_data()
        self.canvas.update_segments(data)

    def _handle_fit(self):
        data = self._gather_input_data()
        self.canvas.update_segments_with_fit(data)

    def _handle_sum_mode_on(self):
        self.canvas.set_sum_mode(True)
        self.sum_btn.hide()
        self.cancel_sum_btn.show()

    def _handle_sum_mode_off(self):
        self.canvas.set_sum_mode(False)
        self.cancel_sum_btn.hide()
        self.sum_btn.show()
