import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel)
from gui_left_window import Left_window
from gui_fourier import GuiFourierMain
from Model.model import Model


class QFApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("C'est fou. Riez!")
        self.resize(1250, 900)
        self.__fourier_main = None
        self.init_gui()
        self.setStyleSheet("background-color: rgb(100,100,100);")

    def init_gui(self):
        # declarations
        centralWidget = QWidget()
        layoutContainer = QHBoxLayout()

        # ajout
        layoutContainer.addWidget(Left_window())
        centralWidget.setLayout(layoutContainer)
        self.__fourier_main = GuiFourierMain()

        layoutContainer.addWidget(self.__fourier_main)

        self.setCentralWidget(centralWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QFApp()
    w.show()
    sys.exit(app.exec())
