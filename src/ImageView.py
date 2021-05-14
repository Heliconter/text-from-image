from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem
from PyQt5.QtCore import Qt, QRectF, pyqtSignal, pyqtSlot, QSizeF

from ImageItem import ImageItem
from FieldItem import FieldItem

from denormalize_rect import denormalize_rect

class ImageView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(600, 400)

        self._scene = QGraphicsScene()
        self.image_item = ImageItem(
            on_rect_start = self.update_rect,
            on_rect_resize = self.update_rect,
            on_rect_end = self.end_rect,
        )
        self._scene.addItem(self.image_item)
        self.setScene(self._scene)

        self.rect_item = None

    rect_set = pyqtSignal(QRectF)

    def update_rect(self, rect: QRectF):
        rect = denormalize_rect(self.image_item.boundingRect().size(), rect)
        if not self.rect_item:
            self.rect_item = FieldItem(rect)
            self._scene.addItem(self.rect_item)
        else:
            self.rect_item.setRect(rect)

    def end_rect(self, rect: QRectF):
        self.update_rect(rect)
        self.rect_set.emit(rect)

    def reset_rect(self):
        if self.rect_item:
            self._scene.removeItem(self.rect_item)
            self.rect_item = None

    def open_image(self, path):
        pixmap = QPixmap(path)
        self.image_item.setPixmap(pixmap)
        self.fitInView(self.image_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.reset_rect()

    def resizeEvent(self, event):
        if self.image_item:
            self.fitInView(self.image_item, Qt.AspectRatioMode.KeepAspectRatio)
