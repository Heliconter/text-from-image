import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PIL import Image
import pytesseract as tess

from ImageView import ImageView


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("text-from-image")

        self.central_widget = QSplitter(self)
        self.setCentralWidget(self.central_widget)

        self.image_view = ImageView()
        self.central_widget.addWidget(self.image_view)

        self.recognized_view = QLabel()
        self.recognized_view.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)
        scroll_area = QScrollArea()
        scroll_area.setMinimumSize(300, 400)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.recognized_view)
        self.central_widget.addWidget(scroll_area)

        self.central_widget.setSizes([10000000, 10000000])
        self.central_widget.setStretchFactor(0, 1)
        self.central_widget.setStretchFactor(1, 1)

        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)

        self.file_menu = QMenu("&File", self)
        self.menubar.addMenu(self.file_menu)

        self.open_image_action = QAction('&Open image', self)
        self.file_menu.addAction(self.open_image_action)
        self.open_image_action.triggered.connect(self.open_image)

    def open_image(self):
        path = QFileDialog.getOpenFileName(None, 'Open File', './', 'Image (*.png *.jpg *jpeg)')[0]

        if path:
            self.image_view.open_image(path)

            img = Image.open(path)
            text = tess.image_to_string(img, lang='eng+rus')
            self.recognized_view.setText(text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
