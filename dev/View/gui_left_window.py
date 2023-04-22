import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot, QSize
from PySide6.QtGui import QIcon, QPainter, QColor
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QSizePolicy)

from gui_left_apps import GuiNavMenu, GuiCustomDrawing


class Left_window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.setMinimumWidth(480)

        self.setMinimumHeight(720)
        self.init_gui()
        self.setStyleSheet("padding-left: 0px; padding-right: 0px; padding-top: 0px; padding-bottom: 0px;")

    def init_gui(self):
        # declarations
        __mainLayout = QVBoxLayout()
        menu = GuiNavMenu()
        drawingBoard = GuiCustomDrawing()
        menu.setContentsMargins(0, 0, 0, 0)
        # ajout
        __mainLayout.addWidget(menu)
        __mainLayout.addWidget(drawingBoard)
        self.setLayout(__mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(163, 13, 149))
