import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QPushButton)

class GuiNavMenu(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        __mainLayout = QHBoxLayout()
        __btnDraw = QPushButton("Dessiner")
        __btnGallery = QPushButton("Galerie")
        __btnFeed = QPushButton("Fil")
        __btnConnectProf = QPushButton("Connexion")