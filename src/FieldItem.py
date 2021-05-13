from PySide2.QtWidgets import QGraphicsTextItem, QGraphicsRectItem, QGraphicsItemGroup, QGraphicsItem, QGraphicsPixmapItem
from PySide2.QtCore import Qt, QRectF
from PySide2.QtGui import QBrush, QPainter, QColor, QPen

class FieldItem(QGraphicsRectItem):
    def __init__(self, rect: QRectF, parent=None):
        super().__init__(parent)

        self.setRect(rect)
        self._rect = rect

        text = QGraphicsTextItem(self)
        text.setParentItem(self)
        text.setPlainText('lsddjfk')
        text.setTextInteractionFlags(Qt.TextEditorInteraction)

    def paint(self, painter: QPainter, option, widget):
        painter.setPen(QPen(Qt.black))
        super().paint(painter, option, widget)
        painter.setBrush(QBrush(QColor(255, 255, 255, 128)))
        painter.drawRect(self.boundingRect())
