import math
from copy import deepcopy

from PySide6.QtCore import Qt, Signal, Slot, QTimer, QPointF
import PySide6
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

        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawPoint(PySide6.QtCore.QPointF(self.height() / 2, self.height() / 2))
        a = self.height() / 2
        painter.drawEllipse(QPointF(65, 65), a, a)


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
        self.path_result = None
        self.path = None
        self.init_gui()

    def init_gui(self):
        __mainLayout = QVBoxLayout()
        self.path = []
        self.path_result = []

        self.is_drawing = False

        # Insertion des boutons dans les layouts
        self.setLayout(__mainLayout)
        self.__timer = QTimer()
        self.__timer.timeout.connect(lambda: self.tick.emit())

    def start_sim(self, vectors):
        self.path_result = []
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
        self.path_result = []
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255))
        if len(self.path) <= 0:
            return

        # placer le dernier point dans le dessin
        self.path_result.append(deepcopy(self.path[-1]))

        # recréer le dessin
        painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        if len(self.path_result) > 1:
            for i in range(1, len(self.path_result)):
                x1, y1 = self.path_result[i - 1][0], self.path_result[i - 1][1]
                x2, y2 = self.path_result[i][0], self.path_result[i][1]
                painter.drawLine(x1, y1, x2, y2)

        # dessin des vecteurs
        for i in range(1, len(self.path)):
            # vecteurs
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.drawLine(self.path[i - 1, 0], self.path[i - 1, 1], self.path[i, 0], self.path[i, 1])

            # cercle autour vecteurs
            painter.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
            center = QPointF(self.path[i - 1, 0], self.path[i - 1, 1])
            radius = math.sqrt(
                (self.path[i, 0] - self.path[i - 1, 0]) ** 2 + (self.path[i, 1] - self.path[i - 1, 1]) ** 2)
            painter.drawEllipse(center, radius, radius)


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

        # events boutons
        self.__btnPlayPause.clicked.connect(lambda: self.clique_btn_play())

        # Insertion des sous-layout dans le main layout
        __mainLayout.addLayout(__topLayout)
        __mainLayout.addLayout(__bottomLayout)
        self.setLayout(__mainLayout)

    def clique_btn_play(self):
        if self.__btnPlayPause.text() == "Play":
            self.__btnPlayPause.setText("Pause")
            return
        self.__btnPlayPause.setText("Play")

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

        # progress
        self.__intervalScroll.setRange(0, 100)
        self.__intervalScroll.setValue(100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("blue"))
