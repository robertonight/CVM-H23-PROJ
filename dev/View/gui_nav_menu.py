import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon, QPainter, QColor
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QPushButton,
                               QSizePolicy)


class GuiNavMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Déclaration du layout et des boutons
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        mainLayout = QHBoxLayout()
        self.setFixedHeight(50)

        # buttons
        taille = 100
        tailleHeight = 30
        self.__btnDraw = QPushButton("Dessiner")
        self.__btnDraw.setFixedWidth(taille)
        self.__btnDraw.setFixedHeight(tailleHeight)

        self.__btnGallery = QPushButton("Galerie")
        self.__btnGallery.setFixedWidth(taille)
        self.__btnGallery.setFixedHeight(tailleHeight)

        self.__btnFeed = QPushButton("Fil")
        self.__btnFeed.setFixedWidth(taille)
        self.__btnFeed.setFixedHeight(tailleHeight)

        self.__btnConnectProf = QPushButton("Connexion")
        self.__btnConnectProf.setFixedWidth(taille)
        self.__btnConnectProf.setFixedHeight(tailleHeight)

        self.__btnQuit = QPushButton("Quitter")
        self.__btnQuit.setFixedWidth(taille)
        self.__btnQuit.setFixedHeight(tailleHeight)

        # Insertion des boutons dans le layout`
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.__btnDraw)
        mainLayout.addWidget(self.__btnGallery)
        mainLayout.addWidget(self.__btnFeed)
        mainLayout.addWidget(self.__btnConnectProf)
        mainLayout.addWidget(self.__btnQuit)
        # mainLayout.addStretch()
        self.setLayout(mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(163, 81, 75))
