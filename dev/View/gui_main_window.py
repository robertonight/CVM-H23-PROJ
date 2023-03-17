import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel)
from gui_left_window import Left_window
from gui_fourier_draw import GuiFourierDraw


class QFApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("C'est fou. Riez!")
        self.resize(1250, 700)
        self.setStyleSheet("background-color: rgb(100,100,100); margin:5px; border:1px solid rgb(0, 0, 0); ")
        self.init_gui()

    def init_gui(self):
        # declarations
        self.centralWidget = QWidget()
        # self.centralWidget.setStyleSheet("background-color:blue")

        self.layoutContainer = QHBoxLayout()

        # ajout
        # self.layoutContainer.addWidget(Left_window())
        self.layoutContainer.addWidget(GuiFourierDraw())
        self.centralWidget.setLayout(self.layoutContainer)
        self.setCentralWidget(self.centralWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QFApp()
    w.show()
    sys.exit(app.exec())
