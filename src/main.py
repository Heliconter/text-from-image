import sys
from typing import Any, Optional
from PyQt5.QtWidgets import QMainWindow, QSplitter, QMenuBar, QMenu, QAction, QFileDialog, QApplication
from PyQt5.QtCore import QRectF, QSizeF, QObject, pyqtSignal, QThread
from PIL import Image
import pytesseract as tess # type: ignore
from Field import RuntimeField 

from ImageView import ImageView
from RecognizedView import RecognizedView
from denormalize_rect import denormalize_rect

class Recognizer(QObject):
    finished = pyqtSignal(str)
    
    def __init__(self, image_path: str, rect: Optional[QRectF] = None):
        super().__init__()

        self.image_path = image_path
        self.rect = rect

    def run(self):
        img = Image.open(self.image_path)
        if self.rect:
            img_size = QSizeF(img.size[0], img.size[1])
            rect = denormalize_rect(img_size, self.rect)
            img = img.crop((
                int(rect.left()),
                int(rect.top()),
                int(rect.right()),
                int(rect.bottom())
            ))
        config = r'--oem 3 --psm 6'
        text = tess.image_to_string(img, lang='eng+rus', config=config) # type: ignore
        self.finished.emit(text)

class Window(QMainWindow):
    def __init__(self, parent: Any = None):
        super().__init__(parent)

        self.setWindowTitle('text-from-image')

        self.central_widget = QSplitter(self)
        self.setCentralWidget(self.central_widget)

        self.image_view = ImageView()
        self.image_view.new_field.connect(self.on_new_field)
        self.central_widget.addWidget(self.image_view)

        self.recognized_view = RecognizedView()
        self.central_widget.addWidget(self.recognized_view)

        self.central_widget.setSizes([10000000, 10000000])
        self.central_widget.setStretchFactor(0, 1)
        self.central_widget.setStretchFactor(1, 1)

        self.menubar = QMenuBar(self)
        self.setMenuBar(self.menubar)

        self.file_menu = QMenu("&File", self)
        self.menubar.addMenu(self.file_menu)

        self.open_image_action = QAction('&Open image', self)
        self.file_menu.addAction(self.open_image_action)
        self.open_image_action.triggered.connect(self.open_image) # type: ignore

    _recognizers: set[Recognizer] = set();
    def remove_recognizer(self, recognizer: Recognizer):
        self._recognizers.remove(recognizer)
    def recognize(self, runtime_field: RuntimeField):
        thread = QThread(self)
        recognizer = Recognizer(self.image_path, runtime_field.field.rect)
        self._recognizers.add(recognizer)
        recognizer.moveToThread(thread)

        thread.started.connect(recognizer.run) # type: ignore

        recognizer.finished.connect(runtime_field.set_recognized)
        recognizer.finished.connect(thread.quit)
        recognizer.finished.connect(recognizer.deleteLater)
        recognizer.destroyed.connect(self.remove_recognizer) # type: ignore
        thread.finished.connect(thread.deleteLater) # type: ignore

        thread.start()

    def on_new_field(self, runtime_field: RuntimeField):
        self.image_changed.connect(runtime_field.underlying_image_changed)
        self.recognized_view.add_field(runtime_field)
        def recognize_in_field():
            runtime_field.set_recognized('Recognizing...')
            self.recognize(runtime_field)
        connection = self.image_changed.connect(recognize_in_field)
        runtime_field.destroyed.connect(lambda: self.disconnect(connection)) # type: ignore
        recognize_in_field()

    image_changed = pyqtSignal()
    def open_image(self):
        path = QFileDialog.getOpenFileName(None, 'Open File', './', 'Image (*.png *.jpg *jpeg)')[0]

        if path:
            self.image_path = path
            self.image_view.open_image(path)
            self.image_changed.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
