from PySide6.QtCore import Signal, Slot
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QSizePolicy)

from gui_left_apps import GuiNavMenu, GuiCustomDrawing


class Left_window(QWidget):
    line_ended = Signal(list)
    undo_pushed = Signal()
    erase_pushed = Signal()
    drawing_saved = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.setMinimumWidth(480)

        self.setMinimumHeight(680)
        self.init_gui()
        self.setStyleSheet("padding-left: 0px; padding-right: 0px; padding-top: 0px; padding-bottom: 0px;")

    def init_gui(self):
        # declarations
        __mainLayout = QVBoxLayout()
        menu = GuiNavMenu()
        self.drawingBoard = GuiCustomDrawing()
        self.drawingBoard.line_ended.connect(self.line_ended.emit)
        self.drawingBoard.undo_pushed.connect(lambda: self.undo_pushed.emit())
        self.drawingBoard.erase_pushed.connect(lambda: self.erase_pushed.emit())
        self.drawingBoard.drawing_saved.connect(self.drawing_saved.emit)
        menu.setContentsMargins(0, 0, 0, 0)
        # ajout
        __mainLayout.addWidget(menu)
        __mainLayout.addWidget(self.drawingBoard)
        self.setLayout(__mainLayout)

    def erase_drawing(self):
        self.drawingBoard.erase_drawing()

    @Slot()
    def undo(self, drawing):
        self.drawingBoard.undo(drawing)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(163, 13, 149))