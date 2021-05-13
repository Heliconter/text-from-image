from PySide2.QtWidgets import QWidget, QLabel, QSizePolicy, QGraphicsPixmapItem, QGraphicsItem
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, QPointF, QRectF
from typing import Callable

def build_rect(p1: QPointF, p2: QPointF) -> QRectF:
    left_top = QPointF(min(p1.x(), p2.x()), min(p1.y(), p2.y()))
    rigth_bottom = QPointF(max(p1.x(), p2.x()), max(p1.y(), p2.y()))
    return QRectF(left_top, rigth_bottom)

def normalize_pos(widget: QGraphicsItem, pos: QPointF) -> QPointF:
    bounding = widget.boundingRect()
    return QPointF(pos.x() / bounding.width(), pos.y() / bounding.height())

class ImageItem(QGraphicsPixmapItem):
    Notification = Callable[[QRectF], None]

    def __init__(
        self,
        parent = None,
        on_rect_start: Notification = None,
        on_rect_move: Notification = None,
        on_rect_end: Notification = None
    ):
        super().__init__(parent)

        self.on_rect_start = on_rect_start
        self.on_rect_move = on_rect_move
        self.on_rect_end = on_rect_end

        self._start: QPointF = None

    def mousePressEvent(self, event):
        if self.on_rect_start and event.buttons() & Qt.LeftButton:
            self._start = normalize_pos(self, event.pos())
            self.on_rect_start(build_rect(self._start, self._start))

    def mouseMoveEvent(self, event):
        if self.on_rect_move and event.buttons() & Qt.LeftButton:
            end = normalize_pos(self, event.pos())
            self.on_rect_move(build_rect(self._start, end))

    def mouseReleaseEvent(self, event):
        if self.on_rect_end and event.button() & Qt.LeftButton:
            end = normalize_pos(self, event.pos())
            rect = build_rect(self._start, end)
            self.on_rect_end(rect)

