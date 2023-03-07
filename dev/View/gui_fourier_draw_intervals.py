import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QToolButton, QScrollBar, QWidget, QFormLayout,
                               QPushButton)


class GuiFourierDrawIntervals(QWidget):
    def __init__(self, parent=None):
        super.__init__(parent)
        __mainLayout = QVBoxLayout()
        self.__infoBtnInterval = QToolButton()
        self.__intervalScroll = QScrollBar()
        __mainLayout.addWidget(self.__infoBtnInterval)
        __mainLayout.addWidget(self.__intervalScroll)
        self.setLayout(__mainLayout)