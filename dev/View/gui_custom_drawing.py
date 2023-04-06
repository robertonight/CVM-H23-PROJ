import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon, QPainter, QColor, QPen
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout)


class GuiCustomDrawing(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Déclaration des layouts et des boutons
        __mainLayout = QVBoxLayout()
        __highLayout = QVBoxLayout()
        __lowLayout = QHBoxLayout()

        self.__eraseBtn = QPushButton("X")
        self.__eraseBtn.setFixedSize(20, 20)
        self.__undoBtn = QPushButton("undo")
        self.__saveBtn = QPushButton("save")

        # Insertion des boutons dans les layouts
        __highLayout.addWidget(self.__eraseBtn)
        __highLayout.addWidget(DrawingWidget())
        __lowLayout.addWidget(self.__undoBtn)
        __lowLayout.addWidget(self.__saveBtn)
        __mainLayout.addLayout(__highLayout)
        __mainLayout.addLayout(__lowLayout)
        self.setLayout(__mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(95, 78, 133))


class DrawingWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = []
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
