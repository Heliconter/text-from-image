from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsSceneMouseEvent
from PyQt5.QtCore import Qt, QPointF, QRectF
from typing import Callable, Optional

def normalize_pos(widget: QGraphicsItem, pos: QPointF) -> QPointF:
    bounding = widget.boundingRect()
    return QPointF(pos.x() / bounding.width(), pos.y() / bounding.height())

class ImageItem(QGraphicsPixmapItem):
    Notification = Callable[[QRectF], None]

    def __init__(
        self,
        parent: Optional[QGraphicsItem] = None,
        on_rect_start: Optional[Notification] = None,
        on_rect_resize: Optional[Notification] = None,
        on_rect_end: Optional[Notification] = None
    ):
        super().__init__(parent)

        self.on_rect_start = on_rect_start
        self.on_rect_resize = on_rect_resize
        self.on_rect_end = on_rect_end

        self._start: Optional[QPointF] = None

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self._start = normalize_pos(self, event.pos())
            if self.on_rect_start:
                self.on_rect_start(QRectF(self._start, self._start).normalized())

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self.on_rect_resize and event.buttons() & Qt.MouseButton.LeftButton:
            end = normalize_pos(self, event.pos())
            if self._start:
                self.on_rect_resize(QRectF(self._start, end).normalized())

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if self.on_rect_end and event.button() & Qt.MouseButton.LeftButton:
            end = normalize_pos(self, event.pos())
            if self._start:
                self.on_rect_end(QRectF(self._start, end).normalized())
