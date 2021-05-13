from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QWidget, QLabel, QHBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsItem
from PySide2.QtCore import Qt, QRectF, QPointF

from ImageItem import ImageItem
from FieldItem import FieldItem

def denormalize_rect(item: QGraphicsItem, rect: QRectF) -> QRectF:
    bounding = item.boundingRect()
    return QRectF(
        rect.x() * bounding.width(),
        rect.y() * bounding.height(),
        rect.width() * bounding.width(),
        rect.height() * bounding.height(),
    )


class ImageView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(600, 400)

        self.scene = QGraphicsScene()
        self.image_item = ImageItem(
            on_rect_start = lambda rect: print('start', rect),
            on_rect_move = lambda rect: print('move', rect),
            on_rect_end = lambda rect: self.add_rect(rect),
        )
        self.scene.addItem(self.image_item)
        # rect = QGraphicsTextItem()
        # rect.setPlainText('0239420834')
        # rect.setTextInteractionFlags(Qt.TextEditorInteraction)
        # rect = FieldItem()
        # self.scene.addItem(rect)
        self.setScene(self.scene)

        self.rects = []

    def add_rect(self, rect: QRectF):
        rect = FieldItem(denormalize_rect(self.image_item, rect))
        self.rects.append(rect)
        self.scene.addItem(rect)

    def open_image(self, path):
        pixmap = QPixmap(path)
        self.image_item.setPixmap(pixmap)
        self.fitInView(self.image_item, Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        if self.image_item:
            self.fitInView(self.image_item, Qt.KeepAspectRatio)
