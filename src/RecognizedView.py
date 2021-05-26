from typing import Optional
from PyQt5.QtWidgets import QGridLayout, QLineEdit, QPushButton, QScrollArea, QLabel, QSizePolicy, QWidget
from PyQt5.QtCore import Qt
from Field import RuntimeField

def create_label() -> QLabel:
    label = QLabel()
    label.setTextInteractionFlags(
        label.textInteractionFlags() | # type: ignore
        Qt.TextInteractionFlag.TextSelectableByMouse |
        Qt.TextInteractionFlag.TextSelectableByKeyboard
    )
    return label

class RecognizedView(QScrollArea):
    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)

        self.container = QWidget()
        self.container_layout = QGridLayout()
        self.container_layout.setColumnStretch(0, 1)
        self.container_layout.setColumnStretch(1, 2)
        self.container.setLayout(self.container_layout)

        self.setMinimumSize(300, 400)
        self.setWidgetResizable(True)
        self.setWidget(self.container)

    def add_field(self, runtime_field: RuntimeField):
        name = QLineEdit()
        name.setText('Area ' + self.container_layout.rowCount().__str__())
        label = create_label()
        delete_button = QPushButton()
        delete_button.setText('X')
        delete_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        rows = self.container_layout.rowCount()
        self.container_layout.addWidget(name, rows, 0)
        self.container_layout.addWidget(label, rows, 1)
        self.container_layout.addWidget(delete_button, rows, 2)

        runtime_field.recognized_changed.connect(label.setText)
        runtime_field.destroyed.connect(name.deleteLater) # type: ignore
        runtime_field.destroyed.connect(delete_button.deleteLater) # type: ignore
        runtime_field.destroyed.connect(label.deleteLater) # type: ignore
        delete_button.clicked.connect(runtime_field.deleteLater) # type: ignore
