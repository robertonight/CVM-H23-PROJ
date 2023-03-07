import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import (QMainWindow, QApplication, QVBoxLayout)


class GuiMainWindow(QMainWindow):
    def __int__(self, parent=None):
        super().__init__(parent)
        # self.
        self.setWindowTitle("C'est fou. Riez!")
        self.mainLayout = QVBoxLayout()








if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = GuiMainWindow()
    w.show()
    sys.exit(app.exec())
