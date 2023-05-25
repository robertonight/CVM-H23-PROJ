# Apps à faire: gui_gallery, gui_profile, gui_profile_preferences, gui_sign_in, gui_sign_up, gui_password_change
import sys

from PySide6.QtCore import Qt, Signal, Slot, QPointF
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QHBoxLayout, QPushButton,
                               QSizePolicy, QInputDialog, QFrame)


class GuiNavMenu(QFrame):
    clicked_feed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # Déclaration du layout et des boutons
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        mainLayout = QHBoxLayout()
        self.setFixedHeight(50)

        # buttons
        taille = 100
        tailleHeight = 30

        self.__btnFeed = QPushButton("Fil")
        self.__btnFeed.setFixedWidth(taille)
        self.__btnFeed.setFixedHeight(tailleHeight)
        self.__btnFeed.clicked.connect(self.clicked_feed)

        self.__btnQuit = QPushButton("Quitter")
        self.__btnQuit.clicked.connect(sys.exit)
        self.__btnQuit.setFixedWidth(taille)
        self.__btnQuit.setFixedHeight(tailleHeight)

        # Insertion des boutons dans le layout
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.__btnFeed)
        mainLayout.addWidget(self.__btnQuit)
        self.setLayout(mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.fillRect(self.rect(), QColor(163, 81, 75))


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

        self.__drawing_canvas = DrawingWidget()
        self.__drawing_canvas.line_ended.connect(self.line_ended)
        __canvasLayout.addStretch()
        __canvasLayout.addWidget(self.__drawing_canvas)
        __canvasLayout.addStretch()

        self.__eraseBtn = QPushButton("X")
        self.__eraseBtn.setStyleSheet("QPushButton {font-size: 15pt; color:red}")
        self.__eraseBtn.clicked.connect(self.erase_pushed.emit)
        self.__eraseBtn.setFixedSize(30, 30)
        __layout_eraseBtn = QHBoxLayout()
        __layout_eraseBtn.addStretch()
        __layout_eraseBtn.addWidget(self.__eraseBtn)

        self.__undoBtn = QPushButton("undo")
        self.__undoBtn.setMinimumWidth(200)
        self.__undoBtn.clicked.connect(self.undo_pushed.emit)
        self.__undoBtn.clicked.connect(self.__drawing_canvas.undo)

        self.__saveBtn = QPushButton("save")
        self.__saveBtn.setMinimumWidth(200)
        self.__saveBtn.clicked.connect(self.save_drawing)

        # Insertion des boutons dans les layouts
        __highLayout.addLayout(__layout_eraseBtn)
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
        drawing_name, ok = QInputDialog.getText(self, 'Sauvegarde', 'Entrez un titre pour votre dessin')
        if ok:
            self.drawing_saved.emit(drawing_name)

    def erase_drawing(self):
        self.__drawing_canvas.erase()

    def undo(self, drawing):
        self.__drawing_canvas.undo(drawing)

    def set_drawing(self, drawing):
        self.__drawing_canvas.set_drawing(drawing)

    def paintEvent(self, event):
        painter = QPainter(self)
        #painter.fillRect(self.rect(), QColor(95, 78, 133))


class DrawingWidget(QWidget):
    line_ended = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = []
        self.is_drawing = False
        self.setFixedHeight(600)
        self.setFixedWidth(700)

    def undo(self):
        if len(self.path) == 1:
            self.erase()
        elif len(self.path) > 0:
            self.path.pop(-1)
        self.update()

    def erase(self):
        self.path = []
        self.update()

    def set_drawing(self, drawing):
        self.path = drawing
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_drawing = True
            if len(self.path) > 0:
                self.path.append([self.path[-1][-1]])
                self.path[-1].append(event.position())
            else:
                self.path.append([event.position()])
            self.update()

    def mouseMoveEvent(self, event):
        if self.is_drawing:
            self.path[-1].append(event.position())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_drawing = False
            if len(self.path) > 1 or len(self.path[-1]) > 1:
                self.path[-1].append(self.path[0][0])
                self.line_ended.emit(self.path[-1])
                self.path[-1].pop(len(self.path[-1]) - 1)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        if len(self.path) > 0:
            self.path[-1].append(self.path[0][0])
            for line in self.path:
                for i in range(1, len(line)):
                    painter.drawLine(line[i - 1], line[i])
            self.path[-1].pop(len(self.path[-1]) - 1)
