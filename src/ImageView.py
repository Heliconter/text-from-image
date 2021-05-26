from typing import Final, Optional
from PyQt5.QtGui import QPixmap, QResizeEvent
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget
from PyQt5.QtCore import Qt, QRectF, pyqtSignal
from Field import Field, RuntimeField
from ImageItem import ImageItem
from FieldItem import FieldItem
from denormalize_rect import denormalize_rect

class ImageView(QGraphicsView):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.setMinimumSize(600, 400)

        self._scene = QGraphicsScene()
        self.image_item = ImageItem(
            # on_rect_start = self.update_rect,
            on_rect_start = self.start_rect_item,
            # on_rect_resize = self.update_rect,
            on_rect_resize = self.update_rect_item,
            on_rect_end = self.end_rect,
        )
        self._scene.addItem(self.image_item)
        self.setScene(self._scene)

        self.rect_item = None

    # def update_rect(self, rect: QRectF):
    #     rect = denormalize_rect(self.image_item.boundingRect().size(), rect)
    #     if not self.rect_item:
    #         self.rect_item = FieldItem(rect)
    #         self._scene.addItem(self.rect_item)
    #     else:
    #         self.rect_item.set_rect(rect)

    new_field = pyqtSignal(RuntimeField)

    def start_rect_item(self, rect: QRectF):
        self.rect_item = FieldItem(QRectF(0, 0, 0, 0))
        self._scene.addItem(self.rect_item)
        self.update_field_item(self.rect_item, rect)
    
    def update_rect_item(self, rect: QRectF):
        assert(self.rect_item)
        self.update_field_item(self.rect_item, rect)

    def update_field_item(self, field_item: FieldItem, rect: QRectF):
        denormalized_rect = denormalize_rect(self.image_item.boundingRect().size(), rect)
        field_item.set_rect(denormalized_rect)

    def end_rect(self, rect: QRectF):
        self.update_rect_item(rect)
        assert(self.rect_item)  
        field_item: Final[FieldItem] = self.rect_item
        runtime_field = RuntimeField(
            field = Field(name = '', rect = rect),
        )
        runtime_field.destroyed.connect(lambda: self._scene.removeItem(field_item)) # type: ignore
        runtime_field.underlying_image_changed.connect(lambda: self.update_field_item(field_item, rect))
        self.new_field.emit(runtime_field)
        self.rect_item = None

    def open_image(self, path: str):
        pixmap = QPixmap(path)
        self.image_item.setPixmap(pixmap)
        self.image_item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.fitInView(self.image_item, Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event: QResizeEvent):
        if self.image_item:
            self.fitInView(self.image_item, Qt.AspectRatioMode.KeepAspectRatio)
