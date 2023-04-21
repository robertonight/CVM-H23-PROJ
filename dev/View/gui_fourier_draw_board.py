import PySide6
from PySide6.QtCore import Qt, QTimer, Signal, Slot
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout)
import time
import numpy as np
from copy import deepcopy


class GuiFourierDrawBoard(QWidget):
    tick = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        __mainLayout = QVBoxLayout()

        # Insertion des boutons dans les layouts
        self.__drawing = FenetreAnimation()
        __mainLayout.addWidget(self.__drawing)
        self.setLayout(__mainLayout)
        self.__timer = QTimer()
        self.__timer.timeout.connect(lambda: self.tick.emit())
        self.__timer.start(33)

    def update_sim(self, vectors):
        vectors[:] = vectors[:] + 100
        self.__drawing.path = vectors
        self.__drawing.update()


class FenetreAnimation(QWidget):
    drawing_done = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = []
        self.redone_d = []

        self.is_drawing = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        # dessin des vecteurs
        if len(self.path) > 0:
            for i in range(1, len(self.path)):
                painter.drawLine(self.path[i - 1, 0], self.path[i - 1, 1], self.path[i, 0], self.path[i, 1])
            # placer le dernier point dans le dessin
            self.redone_d.append(deepcopy(self.path[-1]))
            # recréer le dessin
            pen = QPen(QColor(0, 255, 255), 2, Qt.SolidLine)
            painter.setPen(pen)
            if len(self.redone_d) > 1:
                for i in range(1, len(self.redone_d)):
                    x1 = self.redone_d[i - 1][0]
                    y1 = self.redone_d[i - 1][1]
                    x2 = self.redone_d[i][0]
                    y2 = self.redone_d[i][1]
                    painter.drawLine(x1, y1, x2, y2)
