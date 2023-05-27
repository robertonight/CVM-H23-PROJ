# Nom du fichier: gui_left_window.py
#
# Ce fichier contient les classes GuiFeedMain, DrawingDisplay et DrawingDisplayBoard. Les objets de classe
# DrawingDisplay et DrawingDisplayBoard sont faits pour être insérés dans le GuiFeedMain.
#
# Auteurs: Patrice Gallant et Roberto Nightingale


from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QVBoxLayout, QWidget)

from gui_left_apps import GuiNavMenu, GuiCustomDrawing


class LeftWindow(QWidget):
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
        __menu = GuiNavMenu()
        __menu.clicked_feed.connect(self.cliked_feed)
        self.__drawingBoard = GuiCustomDrawing()
        self.__drawingBoard.line_ended.connect(self.line_ended.emit)
        self.__drawingBoard.undo_pushed.connect(self.undo_pushed.emit)
        self.__drawingBoard.erase_pushed.connect(lambda: self.erase_pushed.emit())
        self.__drawingBoard.drawing_saved.connect(self.drawing_saved.emit)
        __menu.setContentsMargins(0, 0, 0, 0)

        __mainLayout.addWidget(__menu)
        __mainLayout.addWidget(self.__drawingBoard)
        self.setLayout(__mainLayout)

    def erase_drawing(self):
        self.__drawingBoard.erase_drawing()

    def undo(self, drawing):
        self.__drawingBoard.undo(drawing)

    def set_drawing(self, drawing):
        self.__drawingBoard.set_drawing(drawing)
