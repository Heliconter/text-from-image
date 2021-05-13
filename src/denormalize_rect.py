from PySide2.QtCore import QRectF, QSizeF


def denormalize_rect(area: QSizeF, rect: QRectF) -> QRectF:
    return QRectF(
        rect.x() * area.width(),
        rect.y() * area.height(),
        rect.width() * area.width(),
        rect.height() * area.height()
    )