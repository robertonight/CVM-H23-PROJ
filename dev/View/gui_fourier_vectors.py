import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget)


class GuiFourierVectors(QWidget):
    def __init__(self, parent=None):
        super.__init__(parent)
        mainLayout = QVBoxLayout
        self.setLayout(mainLayout)
