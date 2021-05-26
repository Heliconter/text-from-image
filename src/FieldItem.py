from typing import Any, Optional
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsRectItem
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QBrush, QPainter, QColor, QPen


class FieldItem(QGraphicsRectItem):
    def __init__(self, rect: QRectF, parent: Optional[QGraphicsItem] = None):
        super().__init__(parent)

        self.set_rect(rect)

    def set_rect(self, rect: QRectF):
        self.real_rect = rect
        self.setPos(rect.topLeft())
        size = rect.size()
        super().setRect(QRectF(0, 0, size.width(), size.height()))

    def paint(self, painter: QPainter, option: Any, widget: Any):
        painter.setPen(QPen(Qt.GlobalColor.black))
        super().paint(painter, option, widget)
        painter.setBrush(QBrush(QColor(255, 255, 255, 128)))
        painter.drawRect(self.rect())
