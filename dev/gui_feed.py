# à faire: gui_feed_main, gui_feed_gallery, gui_feed_menu
import math
from copy import deepcopy

from PySide6.QtCore import Qt, Signal, Slot, QTimer, QPointF, QLineF
import PySide6
from PySide6.QtCore import Qt, Signal, Slot, QTimer
from PySide6.QtGui import QPainter, QColor, QPixmap, QPen
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QToolButton, QScrollBar, QWidget, QFormLayout,
                               QPushButton, QSizePolicy, QLabel)


class GuiFeedMain(QWidget):
    return_pushed = Signal()

    def __init__(self, drawings, parent=None):
        super().__init__(parent)
        self.__max_grid_col = 4
        self.init_gui(drawings)

    def init_gui(self, drawings):
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        __mainLayout = QVBoxLayout()
        __btnContainer = QHBoxLayout()
        self.__galleryLayout = QGridLayout()
        self.fill_gallery(drawings)
        self.__btnReturn = QPushButton("Return")
        self.__btnReturn.setFixedWidth(100)
        self.__btnReturn.clicked.connect(self.return_pushed)
        __btnContainer.addStretch()
        __btnContainer.addWidget(self.__btnReturn)
        __mainLayout.addLayout(__btnContainer)
        __mainLayout.addLayout(self.__galleryLayout)
        self.setLayout(__mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("red"))

    def fill_gallery(self, drawings):
        grid_row = 1
        grid_column = 1
        if drawings is not None:
            for drawing in drawings:
                new_display = DrawingDisplay(drawing)
                if grid_column > self.__max_grid_col:
                    grid_column = 1
                    grid_row += 1
                new_display.update()
                self.__galleryLayout.addWidget(new_display, grid_row, grid_column)
                grid_column += 1


class DrawingDisplay(QWidget):
    def __init__(self, drawing, parent=None):
        super().__init__(parent)
        self.init_gui(drawing)

    def init_gui(self, drawing):
        __main_layout = QVBoxLayout()
        __drawing_title = QLabel(drawing[1])
        __board_container = QHBoxLayout()
        __drawing_board = DrawingDisplayBoard(drawing[2])
        __drawing_board.setFixedHeight(300)
        __drawing_board.setFixedWidth(210)
        __drawing_board.update()
        __board_container.addStretch()
        __board_container.addWidget(__drawing_board)
        __board_container.addStretch()
        __drawing_date = QLabel(drawing[3])
        __main_layout.addWidget(__drawing_title)
        __main_layout.addLayout(__board_container)
        __main_layout.addWidget(__drawing_date)
        self.setLayout(__main_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("blue"))

class DrawingDisplayBoard(QWidget):
    def __init__(self, drawing, parent=None):
        self.__path = []
        self.set_path(drawing)
        super().__init__(parent)

    def set_path(self, drawing):
        path_lines = drawing.split(":")
        for line in path_lines:
            line_points = line.split(";")
            line_array = []
            for point in line_points:
                coords = point.split(" ")
                if len(coords) == 2:
                    qPoint = QPointF(float(coords[0]), float(coords[1]))
                    line_array.append(qPoint)
            self.__path.append(line_array)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        if len(self.__path) > 0:
            self.__path[-1].append(self.__path[0][0])
            for line in self.__path:
                for i in range(1, len(line)):
                    painter.drawLine(line[i - 1] / 2, line[i] / 2)
            self.__path[-1].pop(len(self.__path[-1]) - 1)
