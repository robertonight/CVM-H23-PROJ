# Nom du fichier: gui_left_apps.py
#
# Ce fichier contient les classes des widgets intérieurs de la fenêtre de gauche de l'interface principale.
# L'idée initiale était qu'il y aurait plusieures interfaces alternatives à cette fenêtre, mais seulement celle de
# CustomDrawing a été faite.
#
# Auteurs: Patrice Gallant et Roberto Nightingale

import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QHBoxLayout, QPushButton,
                               QSizePolicy, QInputDialog, QFrame)


class GuiNavMenu(QFrame):
    clicked_feed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        __mainLayout = QHBoxLayout()
        self.setFixedHeight(50)

        __taille = 100
        __tailleHeight = 30

        self.__btnFeed = QPushButton("Fil")
        self.__btnFeed.setFixedWidth(__taille)
        self.__btnFeed.setFixedHeight(__tailleHeight)
        self.__btnFeed.clicked.connect(self.clicked_feed)

        self.__btnQuit = QPushButton("Quitter")
        self.__btnQuit.clicked.connect(sys.exit)
        self.__btnQuit.setFixedWidth(__taille)
        self.__btnQuit.setFixedHeight(__tailleHeight)

        __mainLayout.setContentsMargins(0, 0, 0, 0)
        __mainLayout.addWidget(self.__btnFeed)
        __mainLayout.addWidget(self.__btnQuit)
        self.setLayout(__mainLayout)


class GuiCustomDrawing(QFrame):
    line_ended = Signal(list)
    undo_pushed = Signal()
    erase_pushed = Signal()
    drawing_saved = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Déclaration des layouts et des boutons
        __mainLayout = QVBoxLayout()
        __mainLayout.setContentsMargins(10, 0, 10, 0)
        __highLayout = QVBoxLayout()
        __highLayout.setContentsMargins(0, 0, 0, 0)
        __canvasLayout = QHBoxLayout()
        __lowLayout = QHBoxLayout()
        __lowLayout.setContentsMargins(0, 0, 0, 0)

        self.__drawingCanvas = DrawingWidget()
        self.__drawingCanvas.line_ended.connect(self.line_ended)
        __canvasLayout.addStretch()
        __canvasLayout.addWidget(self.__drawingCanvas)
        __canvasLayout.addStretch()

        self.__eraseBtn = QPushButton("X")
        self.__eraseBtn.setStyleSheet("QPushButton {font-size: 15pt; color:red}")
        self.__eraseBtn.clicked.connect(self.erase_pushed.emit)
        self.__eraseBtn.setFixedSize(30, 30)
        __layoutEraseBtn = QHBoxLayout()
        __layoutEraseBtn.addStretch()
        __layoutEraseBtn.addWidget(self.__eraseBtn)

        self.__undoBtn = QPushButton("undo")
        self.__undoBtn.setMinimumWidth(200)
        self.__undoBtn.clicked.connect(self.undo_pushed.emit)
        self.__undoBtn.clicked.connect(self.__drawingCanvas.undo)

        self.__saveBtn = QPushButton("save")
        self.__saveBtn.setMinimumWidth(200)
        self.__saveBtn.clicked.connect(self.save_drawing)

        # Insertion des boutons dans les layouts
        __highLayout.addLayout(__layoutEraseBtn)
        __highLayout.addLayout(__canvasLayout)

        __lowLayout.addStretch()
        __lowLayout.addWidget(self.__undoBtn)
        __lowLayout.addStretch()
        __lowLayout.addWidget(self.__saveBtn)
        __lowLayout.addStretch()

        __mainLayout.addLayout(__highLayout)
        __mainLayout.addLayout(__lowLayout)
        self.setLayout(__mainLayout)

    def save_drawing(self):
        drawingName, ok = QInputDialog.getText(self, 'Sauvegarde', 'Entrez un titre pour votre dessin')
        if ok:
            self.drawing_saved.emit(drawingName)

    def erase_drawing(self):
        self.__drawingCanvas.erase()

    def undo(self, drawing):
        self.__drawingCanvas.undo(drawing)

    def set_drawing(self, drawing):
        self.__drawingCanvas.set_drawing(drawing)


class DrawingWidget(QWidget):
    line_ended = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__path = []
        self.__isDrawing = False
        self.setFixedHeight(600)
        self.setFixedWidth(700)

    def undo(self):
        if len(self.__path) == 1:
            self.erase()
        elif len(self.__path) > 0:
            self.__path.pop(-1)
        self.update()

    def erase(self):
        self.__path = []
        self.update()

    def set_drawing(self, drawing):
        self.__path = drawing
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__isDrawing = True
            if len(self.__path) > 0:
                self.__path.append([self.__path[-1][-1]])
                self.__path[-1].append(event.position())
            else:
                self.__path.append([event.position()])
            self.update()

    def mouseMoveEvent(self, event):
        if self.__isDrawing:
            self.__path[-1].append(event.position())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.__isDrawing = False
            if len(self.__path) > 1 or len(self.__path[-1]) > 1:
                self.__path[-1].append(self.__path[0][0])
                self.line_ended.emit(self.__path[-1])
                self.__path[-1].pop(len(self.__path[-1]) - 1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        if len(self.__path) > 0:
            self.__path[-1].append(self.__path[0][0])
            for line in self.__path:
                for i in range(1, len(line)):
                    painter.drawLine(line[i - 1], line[i])
            self.__path[-1].pop(len(self.__path[-1]) - 1)
