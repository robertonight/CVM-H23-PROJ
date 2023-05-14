# à faire: gui_feed_main, gui_feed_gallery, gui_feed_menu
import math
from copy import deepcopy

from PySide6.QtCore import Qt, Signal, Slot, QTimer, QPointF, QLineF
import PySide6
from PySide6.QtCore import Qt, Signal, Slot, QTimer
from PySide6.QtGui import QPainter, QColor, QPixmap, QPen
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QToolButton, QScrollBar, QWidget, QFormLayout,
                               QPushButton, QSizePolicy, QLabel)


class GuiFeedMain(QWidget):

    return_pushed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()


    def init_gui(self):
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        __mainLayout = QVBoxLayout()
        __btnContainer = QHBoxLayout()
        __galleryLayout = QHBoxLayout()
        self.__btnReturn = QPushButton("Return")
        self.__btnReturn.setFixedWidth(100)
        self.__btnReturn.clicked.connect(self.return_pushed)
        __btnContainer.addStretch()
        __btnContainer.addWidget(self.__btnReturn)
        __mainLayout.addWidget(__btnContainer)
        self.setLayout(__mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("red"))