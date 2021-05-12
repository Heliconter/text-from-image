from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPoint

# TODO

class ImageView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setMinimumSize(600, 400)
        self.item = None

        # self.begin, self.destination = QPoint(), QPoint()
        # self.zoom = 1

    def open_image(self, path):
        pixmap = QPixmap(path)
        scene = QGraphicsScene()
        self.item = QGraphicsPixmapItem()
        self.item.setPixmap(pixmap)
        scene.addItem(self.item)
        self.setScene(scene)
        self.fitInView(self.item, Qt.KeepAspectRatio)

    def resizeEvent(self, event):
        if self.item:
            self.fitInView(self.item, Qt.KeepAspectRatio)

    # def mousePressEvent(self, event):
    #     if event.buttons() & Qt.LeftButton:
    #         self.begin = event.pos()
    #         self.destination = self.begin


    # def mouseMoveEvent(self, event):
    #     if event.buttons() & Qt.LeftButton:
    #         self.destination = event.pos()

    # def mouseReleaseEvent(self, event):
    #     if event.button() & Qt.LeftButton:
    #         self.begin, self.destination = QPoint(), QPoint()

    # def wheelEvent(self, event):
