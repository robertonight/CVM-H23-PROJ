# Apps à faire: gui_gallery, gui_profile, gui_profile_preferences, gui_sign_in, gui_sign_up, gui_password_change

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QHBoxLayout, QPushButton,
                               QSizePolicy, QInputDialog)


class GuiNavMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Déclaration du layout et des boutons
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        mainLayout = QHBoxLayout()
        self.setFixedHeight(50)

        # buttons
        taille = 100
        tailleHeight = 30
        self.__btnDraw = QPushButton("Dessiner")
        self.__btnDraw.setFixedWidth(taille)
        self.__btnDraw.setFixedHeight(tailleHeight)

        self.__btnGallery = QPushButton("Galerie")
        self.__btnGallery.setFixedWidth(taille)
        self.__btnGallery.setFixedHeight(tailleHeight)

        self.__btnFeed = QPushButton("Fil")
        self.__btnFeed.setFixedWidth(taille)
        self.__btnFeed.setFixedHeight(tailleHeight)

        self.__btnConnectProf = QPushButton("Connexion")
        self.__btnConnectProf.setFixedWidth(taille)
        self.__btnConnectProf.setFixedHeight(tailleHeight)

        self.__btnQuit = QPushButton("Quitter")
        self.__btnQuit.setFixedWidth(taille)
        self.__btnQuit.setFixedHeight(tailleHeight)

        # Insertion des boutons dans le layout`
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.addWidget(self.__btnDraw)
        mainLayout.addWidget(self.__btnGallery)
        mainLayout.addWidget(self.__btnFeed)
        mainLayout.addWidget(self.__btnConnectProf)
        mainLayout.addWidget(self.__btnQuit)
        # mainLayout.addStretch()
        self.setLayout(mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(163, 81, 75))


class GuiCustomDrawing(QWidget):
    line_ended = Signal(list)
    undo_pushed = Signal()
    erase_pushed = Signal()
    drawing_saved = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Déclaration des layouts et des boutons
        __mainLayout = QVBoxLayout()
        __highLayout = QVBoxLayout()
        __lowLayout = QHBoxLayout()

        self.drawing_canvas = DrawingWidget()
        self.drawing_canvas.line_ended.connect(self.line_ended)

        self.__eraseBtn = QPushButton("X")
        self.__eraseBtn.clicked.connect(lambda: self.erase_pushed.emit())
        self.__eraseBtn.setFixedSize(20, 20)
        self.__undoBtn = QPushButton("undo")
        self.__undoBtn.clicked.connect(lambda: self.undo_pushed.emit())
        self.__undoBtn.clicked.connect(self.drawing_canvas.undo)
        self.__saveBtn = QPushButton("save")
        self.__saveBtn.clicked.connect(self.save_drawing)

        # Insertion des boutons dans les layouts
        __highLayout.addWidget(self.__eraseBtn)
        __highLayout.addWidget(self.drawing_canvas)
        __lowLayout.addWidget(self.__undoBtn)
        __lowLayout.addWidget(self.__saveBtn)
        __mainLayout.addLayout(__highLayout)
        __mainLayout.addLayout(__lowLayout)
        self.setLayout(__mainLayout)

    def save_drawing(self):
        drawing_name, ok = QInputDialog.getText(self, 'Sauvegarde', 'Entrez un titre pour votre dessin')
        if ok:
            self.drawing_saved.emit(drawing_name)

    def erase_drawing(self):
        self.drawing_canvas.erase()

    def undo(self, drawing):
        self.drawing_canvas.undo(drawing)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(95, 78, 133))


class DrawingWidget(QWidget):
    line_ended = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.path = []
        self.is_drawing = False
        self.setFixedHeight(600)
        self.setFixedWidth(420)

    def undo(self):
        if len(self.path) > 0:
            self.path.pop(-1)
        self.update()

    def undo1(self, drawing):
        self.path = drawing
        self.update()

    def erase(self):
        self.path = []
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
