from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PySide2.QtCore import Qt, QRectF, Signal, Slot

from ImageItem import ImageItem
from FieldItem import FieldItem

from denormalize_rect import denormalize_rect

class ImageView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(600, 400)

        self.scene = QGraphicsScene()
        self.image_item = ImageItem(
            # on_rect_start = lambda rect: print('start', rect),
            # on_rect_move = lambda rect: print('move', rect),
            on_rect_end = lambda rect: self.set_rect(rect),
        )
        self.scene.addItem(self.image_item)
        self.setScene(self.scene)

        self.rect_item = None

    rect_set = Signal(QRectF)

    def set_rect(self, rect: QRectF):
        if self.rect_item:
            self.scene.removeItem(self.rect_item)
        self.rect_item = FieldItem(denormalize_rect(self.image_item.boundingRect().size(), rect))
        self.scene.addItem(self.rect_item)
        self.rect_set.emit(rect)

    def open_image(self, path):
        pixmap = QPixmap(path)
        self.image_item.setPixmap(pixmap)
        self.fitInView(self.image_item, Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        if self.image_item:
            self.fitInView(self.image_item, Qt.KeepAspectRatio)
