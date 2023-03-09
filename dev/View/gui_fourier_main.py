import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget)

from gui_fourier_draw import GuiFourierDraw
from gui_fourier_vectors import GuiFourierVectors


class GuiFourierMain(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #Déclaration du layout et des sous-widgets. Les sous-widgets ont leurs propres classes
        __mainLayout = QVBoxLayout
        self.__vectors = GuiFourierVectors()
        self.__drawingSpace = GuiFourierDraw()
        #Insertion des sous-widgets dans le layout
        __mainLayout.addWidget(self.__vectors)
        __mainLayout.addWidget(self.__drawingSpace)
        self.setLayout(__mainLayout)
