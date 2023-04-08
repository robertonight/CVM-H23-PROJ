import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QToolButton, QScrollBar, QWidget, QFormLayout,
                               QPushButton)


class GuiFourierDrawIntervals(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Déclaration du layout et des boutons
        __mainLayout = QVBoxLayout()
        self.__infoBtnInterval = QToolButton()
        self.__intervalScroll = QScrollBar()

        # Insertion des boutons dans le layout
        __mainLayout.addWidget(self.__infoBtnInterval)
        __mainLayout.addWidget(self.__intervalScroll)
        self.setFixedWidth(60)
        self.setLayout(__mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(150, 103, 149))
