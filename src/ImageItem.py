from PySide2.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PySide2.QtCore import Qt, QPointF, QRectF
from typing import Callable

def normalize_pos(widget: QGraphicsItem, pos: QPointF) -> QPointF:
    bounding = widget.boundingRect()
    return QPointF(pos.x() / bounding.width(), pos.y() / bounding.height())

class ImageItem(QGraphicsPixmapItem):
    Notification = Callable[[QRectF], None]

    def __init__(
        self,
        parent = None,
        on_rect_start: Notification = None,
        on_rect_resize: Notification = None,
        on_rect_end: Notification = None
    ):
        super().__init__(parent)

        self.on_rect_start = on_rect_start
        self.on_rect_resize = on_rect_resize
        self.on_rect_end = on_rect_end

        self._start: QPointF = None

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self._start = normalize_pos(self, event.pos())
            if self.on_rect_start:
                self.on_rect_start(QRectF(self._start, self._start).normalized())

    def mouseMoveEvent(self, event):
        if self.on_rect_resize and event.buttons() & Qt.LeftButton:
            end = normalize_pos(self, event.pos())
            self.on_rect_resize(QRectF(self._start, end).normalized())

    def mouseReleaseEvent(self, event):
        if self.on_rect_end and event.button() & Qt.LeftButton:
            end = normalize_pos(self, event.pos())
            self.on_rect_end(QRectF(self._start, end).normalized())

