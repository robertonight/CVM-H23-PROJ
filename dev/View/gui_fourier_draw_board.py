import PySide6
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout)
import time

class GuiFourierDrawBoard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        __mainLayout = QVBoxLayout()

        # Insertion des boutons dans les layouts
        __mainLayout.addWidget(FenetreAnimation())
        self.setLayout(__mainLayout)


class FenetreAnimation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = [PySide6.QtCore.QPointF(100.0, 100.0), PySide6.QtCore.QPointF(200.0, 100.0),
                     PySide6.QtCore.QPointF(200.0, 200.0), PySide6.QtCore.QPointF(100.0, 200.0)]

        self.is_drawing = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_drawing = True
            self.path.append(event.position())
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.path.append(event.position())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            # self.path[-1].append(QtCore.QPointF(self.path[-1]))
            self.is_drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        if len(self.path) > 0:
            for i in range(1, len(self.path)):
                painter.drawLine(self.path[i - 1], self.path[i])
            painter.drawLine(self.path[len(self.path) - 1], self.path[0])
