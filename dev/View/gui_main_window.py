import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QLabel)
from gui_left_window import Left_window


class QFApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("C'est fou. Riez!")
        self.resize(1250, 700)
        self.init_gui()

    def init_gui(self):
        # declarations
        self.centralWidget = QWidget()
        # self.centralWidget.setStyleSheet("background-color:blue")

        self.layoutContainer = QHBoxLayout()
        left_layout = QVBoxLayout()

        # ajout
        left_layout.addWidget(Left_window())
        test = QLabel("HI!")
        test.setStyleSheet("background-color:green")

        # test.setStyleSheet("background-color:blue")
        left_layout.addWidget(test)
        self.layoutContainer.addLayout(left_layout)
        self.centralWidget.setLayout(self.layoutContainer)
        self.setCentralWidget(self.centralWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QFApp()
    w.show()
    sys.exit(app.exec())
