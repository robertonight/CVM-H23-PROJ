import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QToolButton, QScrollBar, QWidget, QFormLayout,
                               QPushButton)


class GuiFourierDrawControls(QWidget):
    def __init__(self,parent=None):
        super.__init__(parent)
        __mainLayout = QVBoxLayout()
        __topLayout = QHBoxLayout()
        __bottomLayout = QHBoxLayout()
        self.__formNbVectors = QFormLayout()
        self.__infoBtnNbVectors = QToolButton()
        self.__btnPrevious = QPushButton()
        self.__btnPlayPause = QPushButton()
        self.__btnNext = QPushButton()
        __topLayout.addWidget(self.__btnPrevious)
        __topLayout.addWidget(self.__btnPlayPause)
        __topLayout.addWidget(self.__btnNext)
        __bottomLayout.addWidget(self.__formNbVectors)
        __bottomLayout.addWidget(self.__infoBtnNbVectors)
        __mainLayout.addLayout(__topLayout)
        __mainLayout.addLayout(__bottomLayout)
        self.setLayout(__mainLayout)
