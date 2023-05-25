from PySide6.QtCore import QPointF
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QPushButton, QSizePolicy, QLabel,
                               QFrame, QScrollArea)
from utils import LinkedList, Node


class GuiFeedMain(QWidget):
    return_pushed = Signal()
    display_right_clicked = Signal(list)

    def __init__(self, drawings, parent=None):
        super().__init__(parent)
        self.__maxGridCol = 4
        self.__linkedList = LinkedList()
        self.__selectedNode = None
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
        currNode = None
        if drawings is not None:
            for drawing in drawings:
                newDisplay = DrawingDisplay(drawing)
                newDisplay.display_left_clicked.connect(self.clicked_display)
                newDisplay.display_right_clicked.connect(self.display_right_clicked.emit)
                if self.__linkedList.head is None:
                    self.__linkedList.head = Node(newDisplay)
                    currNode = self.__linkedList.head
                else:
                    newNode = Node(newDisplay)
                    newNode.previous = currNode
                    currNode.next = newNode
                    currNode = newNode
                newDisplay.node = currNode

    def fill_gallery(self):
        self.__mainLayout.removeWidget(self.__scrollArea)
        self.__scrollArea = QScrollArea()
        __galleryContainer = QWidget()
        __galleryLayout = QGridLayout()
        grid_row = 1
        grid_column = 1
        curr_node = self.__linkedList.head
        while curr_node is not None:
            if grid_column > self.__maxGridCol:
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
        if self.__selectedNode is None:
            node.data.color = QColor(100,150,200)
            node.data.update()
            self.__selectedNode = node
        elif self.__selectedNode is node or self.__selectedNode.previous is node:
            self.__selectedNode.data.color = QColor(150, 150, 150)
            self.__selectedNode.data.update()
            self.__selectedNode = None
        else:
            if self.__selectedNode.previous is None:
                self.__linkedList.head = self.__selectedNode.next
                self.__linkedList.head.previous = None
            else:
                self.__selectedNode.previous.next = self.__selectedNode.next
                if self.__selectedNode.next is not None:
                    self.__selectedNode.next.previous = self.__selectedNode.previous
            self.__selectedNode.next = node.next
            if node.next is not None:
                node.next.previous = self.__selectedNode
            node.next = self.__selectedNode
            self.__selectedNode.previous = node
            self.__selectedNode.data.color = QColor(150, 150, 150)
            self.__selectedNode = None
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
        __title_container = QHBoxLayout()
        __drawing_title = QLabel(drawing[1])
        __title_container.addStretch()
        __title_container.addWidget(__drawing_title)
        __title_container.addStretch()
        __board_container = QHBoxLayout()
        self.__drawing_board = DrawingDisplayBoard(drawing[2])
        self.__drawing_board.setFixedHeight(300)
        self.__drawing_board.setFixedWidth(350)
        self.__drawing_board.update()
        __board_container.addStretch()
        __board_container.addWidget(self.__drawing_board)
        __board_container.addStretch()
        __date_container = QHBoxLayout()
        __drawing_date = QLabel(drawing[3])
        __date_container.addStretch()
        __date_container.addWidget(__drawing_date)
        __date_container.addStretch()
        __main_layout.addLayout(__title_container)
        __main_layout.addLayout(__board_container)
        __main_layout.addLayout(__date_container)
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
