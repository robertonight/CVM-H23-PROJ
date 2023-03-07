import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout, QPushButton, QWidget, QHBoxLayout)


class QFApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("C'est fou. Riez!")
        self.initGUI()

    def initGUI(self):
        self.centralWidget = QWidget()
        self.layoutContainer = QHBoxLayout()
        self.centralWidget.setLayout(self.layoutContainer)
        self.setCentralWidget(self.centralWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = QFApp()
    w.show()
    sys.exit(app.exec())
