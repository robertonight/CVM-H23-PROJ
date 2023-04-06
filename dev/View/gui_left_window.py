import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot, QSize
from PySide6.QtGui import QIcon, QPainter, QColor
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QSizePolicy)

from gui_nav_menu import GuiNavMenu
from gui_custom_drawing import GuiCustomDrawing


class Left_window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.setMinimumWidth(480)

        self.setMinimumHeight(720)
        self.init_gui()
        self.setStyleSheet("margin-left: 0px; margin-right: 0px; margin-top: 0px; margin-bottom: 0px;")

    def init_gui(self):
        # declarations
        __mainLayout = QVBoxLayout()
        menu = GuiNavMenu()
        drawingBoard = GuiCustomDrawing()

        # ajout
        __mainLayout.addWidget(menu)
        __mainLayout.addWidget(drawingBoard)
        self.setLayout(__mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(163, 13, 149))
