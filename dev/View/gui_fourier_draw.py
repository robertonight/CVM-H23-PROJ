import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QToolButton, QScrollBar, QWidget, QFormLayout,
                               QPushButton, QSizePolicy, QLabel)
from PySide6.QtGui import QPainter, QColor, QImage, QPolygon, QPixmap

from gui_fourier_draw_controls import GuiFourierDrawControls
from gui_fourier_draw_intervals import GuiFourierDrawIntervals


class GuiFourierDraw(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.setMinimumWidth(800)
        __mainLayout = QVBoxLayout()
        __topLayout = QHBoxLayout()
        self.__guiIntervals = GuiFourierDrawIntervals()
        self.__canvas = QLabel()
        self.__canvas.setPixmap(QPixmap())
        self.__guiControls = GuiFourierDrawControls()
        __topLayout.addWidget(self.__guiIntervals)
        __topLayout.addWidget(self.__canvas)
        __mainLayout.addLayout(__topLayout)
        __mainLayout.addWidget(self.__guiControls)
        self.setLayout(__mainLayout)
