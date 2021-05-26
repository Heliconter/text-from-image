from typing import Optional
from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QLineEdit, QPushButton, QScrollArea, QLabel, QSizePolicy, QVBoxLayout, QWidget
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
        name.setText(runtime_field.field.name)
        label = create_label()
        delete_button = QPushButton()
        delete_button.setText('X')
        delete_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)

        rows = self.container_layout.rowCount()
        self.container_layout.addWidget(name, rows, 0)
        self.container_layout.addWidget(label, rows, 1)
        self.container_layout.addWidget(delete_button, rows, 2)

        # line.addWidget(name)
        # line.addWidget(label)
        # line.addWidget(delete_button)
        # self.container_layout.addLayout(line)

        runtime_field.recognized_changed.connect(lambda text: label.setText(text))
        def on_field_delete():
            # self.container_layout.removeItem(line)
            # line.deleteLater()
            name.deleteLater()
            delete_button.deleteLater()
            label.deleteLater()
        runtime_field.destroyed.connect(on_field_delete) # type: ignore
        delete_button.clicked.connect(lambda: runtime_field.deleteLater()) # type: ignore
