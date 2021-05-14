from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QRectF, QSizeF
from PyQt5.QtGui import QBrush, QPainter, QColor, QPen, QTextDocument


class FieldItem(QGraphicsRectItem):
    def __init__(self, rect: QRectF, parent=None):
        super().__init__(parent)

        self.setRect(rect)

        # text = QGraphicsTextItem(self)
        # text.document().setPageSize(self.rect().size())
        # text.setPlainText('lsddjfk')
        # text.setTextInteractionFlags(Qt.TextEditorInteraction)

    def setRect(self, rect: QRectF):
        self.setPos(rect.topLeft())
        size = rect.size()
        super().setRect(QRectF(0, 0, size.width(), size.height()))

    def paint(self, painter: QPainter, option, widget):
        painter.setPen(QPen(Qt.GlobalColor.black))
        super().paint(painter, option, widget)
        painter.setBrush(QBrush(QColor(255, 255, 255, 128)))
        painter.drawRect(self.rect())
