import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QApplication, QVBoxLayout, QHBoxLayout, QToolButton, QScrollBar, QWidget, QFormLayout,
                               QPushButton)


class GuiFourierDrawControls(QWidget):
    def __init__(self,parent=None):
        super.__init__(parent)
        #Déclaration des layouts
        __mainLayout = QVBoxLayout()
        __topLayout = QHBoxLayout()
        __bottomLayout = QHBoxLayout()
        #Déclaration des boutons
        self.__formNbVectors = QFormLayout()
        self.__infoBtnNbVectors = QToolButton()
        self.__btnPrevious = QPushButton()
        self.__btnPlayPause = QPushButton()
        self.__btnNext = QPushButton()
        #Insertion des boutons dans les layouts
        __topLayout.addWidget(self.__btnPrevious)
        __topLayout.addWidget(self.__btnPlayPause)
        __topLayout.addWidget(self.__btnNext)
        __bottomLayout.addWidget(self.__formNbVectors)
        __bottomLayout.addWidget(self.__infoBtnNbVectors)
        #Insertion des sous-layout dans le main layout
        __mainLayout.addLayout(__topLayout)
        __mainLayout.addLayout(__bottomLayout)
        self.setLayout(__mainLayout)
