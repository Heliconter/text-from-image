import sys
from typing import Any, Callable, Optional
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
        text = tess.image_to_string(img, lang='eng+rus') # type: ignore
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

    def recognize(self, rect: QRectF, callback: Callable[[str], Any]):
        self._thread = QThread()
        self.recognizer = Recognizer(self.image_path, rect)
        self.recognizer.moveToThread(self._thread)

        self._thread.started.connect(self.recognizer.run) # type: ignore
        self.recognizer.finished.connect(lambda text: self._thread.quit())

        self.recognizer.finished.connect(lambda text: callback(text))

        self._thread.start()

    def on_new_field(self, runtime_field: RuntimeField):
        self.image_changed.connect(runtime_field.underlying_image_changed)
        self.recognized_view.add_field(runtime_field)
        def recognize_in_field():
            runtime_field.set_recognized('Recognizing...')
            self.recognize(runtime_field.field.rect, lambda text: runtime_field.set_recognized(text))
        self.image_changed.connect(recognize_in_field)
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
