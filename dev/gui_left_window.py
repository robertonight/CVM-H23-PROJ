from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QSizePolicy, QFrame)

from gui_left_apps import GuiNavMenu, GuiCustomDrawing


class Left_window(QWidget):
    line_ended = Signal(list)
    undo_pushed = Signal()
    erase_pushed = Signal()
    drawing_saved = Signal(str)
    cliked_feed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        # declarations
        __mainLayout = QVBoxLayout()
        menu = GuiNavMenu()
        menu.clicked_feed.connect(self.cliked_feed)
        self.drawingBoard = GuiCustomDrawing()
        self.drawingBoard.line_ended.connect(self.line_ended.emit)
        self.drawingBoard.undo_pushed.connect(self.undo_pushed.emit)
        self.drawingBoard.erase_pushed.connect(lambda: self.erase_pushed.emit())
        self.drawingBoard.drawing_saved.connect(self.drawing_saved.emit)
        menu.setContentsMargins(0, 0, 0, 0)
        # ajout
        __mainLayout.addWidget(menu)
        __mainLayout.addWidget(self.drawingBoard)
        self.setLayout(__mainLayout)

    def erase_drawing(self):
        self.drawingBoard.erase_drawing()

    def undo(self, drawing):
        self.drawingBoard.undo(drawing)

    def set_drawing(self, drawing):
        self.drawingBoard.set_drawing(drawing)
