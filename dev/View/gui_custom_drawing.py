import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout)


class GuiCustomDrawing(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #Déclaration des layouts et des boutons
        __mainLayout = QVBoxLayout()
        __highLayout = QHBoxLayout()
        self.__eraseBtn = QPushButton("X")
        __lowLayout = QHBoxLayout()
        self.__undoBtn = QPushButton("undo")
        self.__saveBtn = QPushButton("save")
        #Insertion des boutons dans les layouts
        __highLayout.addWidget(self.__eraseBtn)
        __lowLayout.addWidget(self.__undoBtn)
        __lowLayout.addWidget(self.__saveBtn)
        __mainLayout.addLayout(__highLayout)
        __mainLayout.addLayout(__lowLayout)
        self.setLayout(__mainLayout)
