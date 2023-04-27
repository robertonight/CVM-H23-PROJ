from copy import deepcopy

from PySide6.QtCore import Qt, Signal, Slot, QTimer
from PySide6.QtGui import QPainter, QColor, QPixmap, QPen
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QToolButton, QScrollBar, QWidget, QFormLayout,
                               QPushButton, QSizePolicy, QLabel)


class GuiFourierMain(QWidget):
    """
    JAUNE
    Fenêtre se trouvant à droite. Elle affiche tout ce qui concerne Fourier
    """

    tick = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__fourier_draw = None
        self.__vectors = None
        self.init_gui()

    def init_gui(self):
        # Déclaration du layout et des sous-widgets. Les sous-widgets ont leurs propres classes
        __mainLayout = QVBoxLayout()
        self.__vectors = GuiFourierVectors()  #
        self.__fourier_draw = GuiFourierDraw()  #
        # Insertion des sous-widgets dans le layout
        __mainLayout.addWidget(self.__vectors)
        __mainLayout.addWidget(self.__fourier_draw)
        self.setLayout(__mainLayout)
        self.__fourier_draw.tick.connect(self.tick.emit)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("yellow"))

    def update_sim(self, vectors):
        self.__fourier_draw.update_sim(vectors)

    def start_sim(self, vectors):
        self.__fourier_draw.start_sim(vectors)

    def erase_drawing(self):
        self.__fourier_draw.erase_drawing()


class GuiFourierVectors(QWidget):
    """
    TURQUOISE
    Vecteurs sur le haut de l'animation qui font le dessin, mais séparés.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()

    def init_gui(self):
        self.setLayout(QVBoxLayout())
        self.setFixedHeight(130)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("turquoise"))


class GuiFourierDraw(QWidget):
    tick = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.setFixedHeight(700)
        self.setFixedWidth(800)
        __mainLayout = QVBoxLayout()
        __topLayout = QHBoxLayout()
        self.__guiIntervals = GuiFourierDrawIntervals()  #
        self.__canvas = QLabel()
        self.__canvas.setPixmap(QPixmap())
        self.__guiControls = GuiFourierDrawControls()  #
        self.__drawBoard = GuiFourierDrawBoard()  #
        self.__drawBoard.tick.connect(lambda: self.tick.emit())
        __topLayout.addWidget(self.__guiIntervals)
        __topLayout.addWidget(self.__drawBoard)
        __mainLayout.addLayout(__topLayout)
        __mainLayout.addWidget(self.__guiControls)
        self.setLayout(__mainLayout)

    def erase_drawing(self):
        self.__drawBoard.erase_drawing()

    def start_sim(self, vectors):
        self.__drawBoard.start_sim(vectors)

    def update_sim(self, vectors):
        self.__drawBoard.update_sim(vectors)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("green"))


class GuiFourierDrawBoard(QWidget):
    """
    Couleur: BLANC
    S'occupe d'afficher les fleches qui sont attachées pour faire dessin
    """
    tick = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__timer = None
        self.is_drawing = None
        self.redone_d = None
        self.path = None
        self.init_gui()

    def init_gui(self):
        __mainLayout = QVBoxLayout()
        self.path = []
        self.redone_d = []

        self.is_drawing = False

        # Insertion des boutons dans les layouts
        self.setLayout(__mainLayout)
        self.__timer = QTimer()
        self.__timer.timeout.connect(lambda: self.tick.emit())

    def start_sim(self, vectors):
        self.redone_d = []
        vectors[:] = vectors[:] + [100, 0]
        self.path = vectors
        self.__timer.start(33)

    def stop_sim(self):
        self.__timer.stop()

    def update_sim(self, vectors):
        vectors[:] = vectors[:] + [100, 0]
        self.path = vectors
        self.update()

    def erase_drawing(self):
        self.stop_sim()
        self.path = []
        self.redone_d = []
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        # dessin des vecteurs
        if len(self.path) > 0:
            for i in range(1, len(self.path)):
                painter.drawLine(self.path[i - 1, 0], self.path[i - 1, 1], self.path[i, 0], self.path[i, 1])
            # placer le dernier point dans le dessin
            self.redone_d.append(deepcopy(self.path[-1]))
            # recréer le dessin
            pen = QPen(QColor(0, 255, 255), 3, Qt.SolidLine)
            painter.setPen(pen)
            if len(self.redone_d) > 1:
                for i in range(1, len(self.redone_d)):
                    x1 = self.redone_d[i - 1][0]
                    y1 = self.redone_d[i - 1][1]
                    x2 = self.redone_d[i][0]
                    y2 = self.redone_d[i][1]
                    painter.drawLine(x1, y1, x2, y2)


class GuiFourierDrawControls(QWidget):
    """
    ROUGE
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Déclaration des layouts
        __mainLayout = QVBoxLayout()
        __topLayout = QHBoxLayout()
        __bottomLayout = QHBoxLayout()

        # Déclaration des boutons
        self.__formNbVectors = QFormLayout()
        self.__infoBtnNbVectors = QPushButton("?")
        self.__btnPrevious = QPushButton("Previous")
        self.__btnPlayPause = QPushButton("Play")
        self.__btnNext = QPushButton("Next")
        self.setFixedHeight(60)

        # Insertion des boutons dans les layouts
        __topLayout.addWidget(self.__btnPrevious)
        __topLayout.addWidget(self.__btnPlayPause)
        __topLayout.addWidget(self.__btnNext)
        __bottomLayout.addLayout(self.__formNbVectors)
        __bottomLayout.addWidget(self.__infoBtnNbVectors)

        # Insertion des sous-layout dans le main layout
        __mainLayout.addLayout(__topLayout)
        __mainLayout.addLayout(__bottomLayout)
        self.setLayout(__mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("red"))


class GuiFourierDrawIntervals(QWidget):
    """
    BLEU
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Déclaration du layout et des boutons
        __mainLayout = QVBoxLayout()
        self.__infoBtnInterval = QToolButton()
        self.__intervalScroll = QScrollBar()

        # Insertion des boutons dans le layout
        __mainLayout.addWidget(self.__infoBtnInterval)
        __mainLayout.addWidget(self.__intervalScroll)
        self.setFixedWidth(60)
        self.setLayout(__mainLayout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("blue"))
