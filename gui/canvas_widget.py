from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QFont
from PyQt5.QtCore import Qt, QRectF

class CanvasWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.segments = []

    def update_segments(self, segments):
        self.segments = segments
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        font = QFont("Arial", 10)
        painter.setFont(font)

        margin = 120  # 左側のラベル分余白
        spacing = 100
        top_margin = 40

        for idx, seg in enumerate(self.segments):
            y_base = top_margin + idx * spacing
            label = seg['label']
            values = seg.get('values', [])
            ratios = seg.get('ratios', [])
            uppers = seg.get('uppers', [])

            x = margin
            y = y_base

            # 左ラベル（折り返しあり）
            if label:
                label_rect = QRectF(10, y - 25, margin - 20, 50)
                painter.drawText(label_rect, Qt.AlignRight | Qt.AlignVCenter | Qt.TextWordWrap, label)

            # 長さ計算
            try:
                nums = [float(v) for v in values if v]
            except ValueError:
                nums = []
            if not nums:
                try:
                    nums = [float(r) for r in ratios if r]
                except ValueError:
                    nums = []

            total = sum(nums) if nums else len(ratios)
            if total == 0:
                continue

            for i, val in enumerate(nums):
                width = val / total * 200
                x0 = x
                x1 = x + width

                # 線分本体
                painter.setPen(QPen(Qt.black, 2))
                painter.drawLine(int(x0), int(y), int(x1), int(y))

                # 区切り縦線
                painter.drawLine(int(x0), y - 5, int(x0), y + 5)
                if i == len(nums) - 1:
                    painter.drawLine(int(x1), y - 5, int(x1), y + 5)

                # 上ラベル（上側に折り返し表示）
                if i < len(uppers):
                    upper_text = uppers[i]
                    upper_rect = QRectF(x0, y - 45, width, 20)
                    painter.drawText(upper_rect, Qt.AlignCenter | Qt.TextWordWrap, upper_text)

                # 値（線上に表示）
                if i < len(values) and values[i]:
                    val_rect = QRectF(x0, y - 25, width, 20)
                    painter.drawText(val_rect, Qt.AlignCenter, values[i])

                # 比（線下に表示）
                if i < len(ratios) and ratios[i]:
                    ratio_rect = QRectF(x0, y + 5, width, 20)
                    painter.drawText(ratio_rect, Qt.AlignCenter, ratios[i])

                x = x1

        painter.end()
