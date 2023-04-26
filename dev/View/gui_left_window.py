from PySide6.QtCore import Signal
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QSizePolicy)

from gui_left_apps import GuiNavMenu, GuiCustomDrawing


class Left_window(QWidget):
    line_ended = Signal(list)
    undo_pushed = Signal()
    erase_pushed = Signal()

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
        drawingBoard = GuiCustomDrawing()
        drawingBoard.line_ended.connect(lambda: self.line_ended.emit())
        drawingBoard.undo_pushed.connect(lambda: self.undo_pushed.emit())
        drawingBoard.erase_pushed.connect(lambda: self.erase_pushed.emit())
        menu.setContentsMargins(0, 0, 0, 0)
        # ajout
        __mainLayout.addWidget(menu)
        __mainLayout.addWidget(drawingBoard)
        self.setLayout(__mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(163, 13, 149))
