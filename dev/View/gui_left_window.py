import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout)

from gui_nav_menu import GuiNavMenu
from gui_custom_drawing import GuiCustomDrawing


class Left_window(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        mainLayout = QVBoxLayout()
        menu = GuiNavMenu()
        drawingBoard = GuiCustomDrawing()
        mainLayout.addWidget(menu)
        mainLayout.addWidget(drawingBoard)
        