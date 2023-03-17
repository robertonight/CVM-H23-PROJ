import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QPushButton,
                               QSizePolicy)


class GuiNavMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        #Déclaration du layout et des boutons
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        __mainLayout = QHBoxLayout()
        self.__btnDraw = QPushButton("Dessiner")
        self.__btnGallery = QPushButton("Galerie")
        self.__btnFeed = QPushButton("Fil")
        self.__btnConnectProf = QPushButton("Connexion")
        self.__btnQuit = QPushButton("Quitter")
        #Insertion des boutons dans le layout
        __mainLayout.addWidget(self.__btnDraw)
        __mainLayout.addWidget(self.__btnGallery)
        __mainLayout.addWidget(self.__btnFeed)
        __mainLayout.addWidget(self.__btnConnectProf)
        __mainLayout.addWidget(self.__btnQuit)
        self.setLayout(__mainLayout)
