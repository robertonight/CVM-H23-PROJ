# à faire: gui_feed_main, gui_feed_gallery, gui_feed_menu
import math
from copy import deepcopy

from PySide6.QtCore import Qt, Signal, Slot, QTimer, QPointF, QLineF
import PySide6
from PySide6.QtCore import Qt, Signal, Slot, QTimer
from PySide6.QtGui import QPainter, QColor, QPixmap, QPen
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QToolButton, QScrollBar, QWidget, QFormLayout,
                               QPushButton, QSizePolicy, QLabel, QFrame, QScrollArea)
from utils import LinkedList, Node


class GuiFeedMain(QWidget):
    return_pushed = Signal()
    display_right_clicked = Signal(list)

    def __init__(self, drawings, parent=None):
        super().__init__(parent)
        self.__max_grid_col = 4
        self.__linked_list = LinkedList()
        self.__selected_node = None
        self.init_gui(drawings)

    def init_gui(self, drawings):
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.__mainLayout = QVBoxLayout()
        __btnContainer = QHBoxLayout()
        self.__scrollArea = QScrollArea()
        __galleryContainer = QWidget()
        self.__scrollArea.setWidget(__galleryContainer)
        self.__btnReturn = QPushButton("Return")
        self.__btnReturn.setFixedWidth(100)
        self.__btnReturn.clicked.connect(self.return_pushed)
        __btnContainer.addStretch()
        __btnContainer.addWidget(self.__btnReturn)
        self.__mainLayout.addLayout(__btnContainer)
        self.create_linked_list(drawings)
        self.fill_gallery()
        self.setLayout(self.__mainLayout)

    def create_linked_list(self, drawings):
        curr_node = None
        if drawings is not None:
            for drawing in drawings:
                new_display = DrawingDisplay(drawing)
                new_display.display_left_clicked.connect(self.clicked_display)
                new_display.display_right_clicked.connect(self.display_right_clicked.emit)
                if self.__linked_list.head is None:
                    self.__linked_list.head = Node(new_display)
                    curr_node = self.__linked_list.head
                else:
                    new_node = Node(new_display)
                    new_node.previous = curr_node
                    curr_node.next = new_node
                    curr_node = new_node
                new_display.node = curr_node

    def fill_gallery(self):
        self.__mainLayout.removeWidget(self.__scrollArea)
        self.__scrollArea = QScrollArea()
        __galleryContainer = QWidget()
        __galleryLayout = QGridLayout()
        grid_row = 1
        grid_column = 1
        curr_node = self.__linked_list.head
        while curr_node is not None:
            if grid_column > self.__max_grid_col:
                grid_column = 1
                grid_row += 1
            __galleryLayout.addWidget(curr_node.data, grid_row, grid_column)
            curr_node.data.update()
            grid_column += 1
            curr_node = curr_node.next
        __galleryContainer.setLayout(__galleryLayout)
        self.__scrollArea.setWidget(__galleryContainer)
        self.__mainLayout.addWidget(self.__scrollArea)

    def clicked_display(self, node):
        if self.__selected_node is None:
            node.data.color = QColor(100,150,200)
            node.data.update()
            self.__selected_node = node
        elif self.__selected_node is node or self.__selected_node.previous is node:
            self.__selected_node.data.color = QColor(150,150,150)
            self.__selected_node.data.update()
            self.__selected_node = None
        else:
            if self.__selected_node.previous is None:
                self.__linked_list.head = self.__selected_node.next
                self.__linked_list.head.previous = None
            else:
                self.__selected_node.previous.next = self.__selected_node.next
                if self.__selected_node.next is not None:
                    self.__selected_node.next.previous = self.__selected_node.previous
            self.__selected_node.next = node.next
            if node.next is not None:
                node.next.previous = self.__selected_node
            node.next = self.__selected_node
            self.__selected_node.previous = node
            self.__selected_node.data.color = QColor(150,150,150)
            self.__selected_node = None
            self.fill_gallery()

class DrawingDisplay(QFrame):

    display_left_clicked = Signal(Node)
    display_right_clicked = Signal(list)

    def __init__(self, drawing, parent=None):
        self.__color = QColor(150,150,150)
        self.__node = None
        super().__init__(parent)
        self.setStyleSheet("QLabel {background-color: rgba(0,0,0,0);}")
        self.init_gui(drawing)

    def init_gui(self, drawing):
        __main_layout = QVBoxLayout()
        __drawing_title = QLabel(drawing[1])
        __board_container = QHBoxLayout()
        self.__drawing_board = DrawingDisplayBoard(drawing[2])
        self.__drawing_board.setFixedHeight(300)
        self.__drawing_board.setFixedWidth(350)
        self.__drawing_board.update()
        __board_container.addStretch()
        __board_container.addWidget(self.__drawing_board)
        __board_container.addStretch()
        __drawing_date = QLabel(drawing[3])
        __main_layout.addWidget(__drawing_title)
        __main_layout.addLayout(__board_container)
        __main_layout.addWidget(__drawing_date)
        self.setLayout(__main_layout)

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
        self.__color = color

    @property
    def node(self):
        return self.__node

    @node.setter
    def node(self, node):
        self.__node = node

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.display_left_clicked.emit(self.__node)
        elif event.button() == Qt.RightButton:
            self.display_right_clicked.emit(self.__drawing_board.path)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), self.__color)


class DrawingDisplayBoard(QWidget):
    def __init__(self, drawing, parent=None):
        self.__path = []
        self.path = drawing
        super().__init__(parent)

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, drawing):
        path_lines = drawing.split(":")
        for line in path_lines:
            line_points = line.split(";")
            line_array = []
            for point in line_points:
                coords = point.split(" ")
                if len(coords) == 2:
                    qPoint = QPointF(float(coords[0]), float(coords[1]))
                    line_array.append(qPoint)
            if len(line_array) > 0:
                self.__path.append(line_array)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255,255,255))

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        if len(self.__path) > 0:
            self.__path[-1].append(self.__path[0][0])
            for line in self.__path:
                for i in range(1, len(line)):
                    painter.drawLine(line[i - 1] / 2, line[i] / 2)
            self.__path[-1].pop(len(self.__path[-1]) - 1)
