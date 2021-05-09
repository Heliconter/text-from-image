from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QTransform
from PyQt5.QtWidgets import QGraphicsView, QWidget
from PyQt5 import QtCore ,Qt
from PyQt5.QtCore import Qt

class GraphicsView(QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)

        self.setGeometry(QtCore.QRect(5, 5, 810, 550))
        self.setObjectName("graphicsView")

        self.begin, self.destination = QPoint(), QPoint()
        self.zoom = 1


    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.begin = event.pos()
            self.destination = self.begin


    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.destination = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() & Qt.LeftButton:
            self.begin, self.destination = QPoint(), QPoint()

    def wheelEvent(self, event):
        # print(event.angleDelta().y())
        print(self.zoom)



