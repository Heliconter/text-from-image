from dataclasses import dataclass
from typing import Any
from PyQt5.QtCore import QObject, QRectF, pyqtSignal

@dataclass
class Field:
    name: str
    rect: QRectF

class RuntimeField(QObject):
    def __init__(self, field: Field, parent: Any = None) -> None:
        super().__init__(parent)
        self.field = field

    recognized_changed = pyqtSignal(str)
    underlying_image_changed = pyqtSignal()
    name_changed = pyqtSignal(str)

    def set_recognized(self, text: str):
        self.recognized_changed.emit(text)

    def set_name(self, new_name: str):
        self.field.name = new_name
        self.name_changed.emit(new_name)

