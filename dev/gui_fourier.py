import math
from copy import deepcopy

import numpy as np
from PySide6.QtCore import Qt, Signal, Slot, QTimer, QPointF, QLineF
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
    play_pressed = Signal()
    previous_pressed = Signal()
    next_pressed = Signal()

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
        self.__fourier_draw.play_pressed.connect(self.play_pressed)
        self.__fourier_draw.pause_pressed.connect(self.stop_sim)
        self.__fourier_draw.previous_pressed.connect(self.previous_pressed)
        self.__fourier_draw.next_pressed.connect(self.next_pressed)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("yellow"))

    @Slot()
    def update_sim(self, vectors, interval):
        self.__fourier_draw.update_sim(vectors[:, 2:], interval)
        self.__vectors.update_sim(vectors[:, 0:2])

    @Slot()
    def start_sim(self, vectors, interval):
        self.__fourier_draw.start_sim(vectors[:, 2:], interval)
        self.__vectors.update_sim(vectors[:, 0:2])

    @Slot()
    def stop_sim(self):
        self.__fourier_draw.stop_sim()

    @Slot()
    def reset_drawing(self):
        self.__fourier_draw.erase_drawing()

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
        self._angle_vectors: np.ndarray = np.zeros(0)

    def init_gui(self):
        self.setLayout(QVBoxLayout())
        self.setFixedHeight(130)

    def update_sim(self, vectors):
        self._angle_vectors = vectors
        self._angle_vectors = self._angle_vectors[self._angle_vectors[:, 0].argsort()]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("turquoise"))
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        if self._angle_vectors.size != 0:
            for i in range(self._angle_vectors[:, 0].size):
                painter.drawPoint(QPointF(self.height() / 2 + (i * self.height()), self.height() / 2))
                painter.drawEllipse(QPointF(self.height() / 2 + (i * self.height()), self.height() / 2),
                                    self.height() / 2 - 2, self.height() / 2 - 2)

                line = QLineF(QPointF(0, 0), QPointF(1, 1))
                line.setP1(QPointF(int(self.height() / 2 + (i * self.height())), self.height() / 2))
                line.setAngle(self._angle_vectors[i, 1] * (180 / np.pi))
                line.setLength(self.height() / 2 - 2)
                painter.drawLine(line)

            # print(self._angle_vectors[4, 1])
            #
            # sizeTest = (rayon * 3) + 4
            # painter.drawPoint(PySide6.QtCore.QPointF(sizeTest, rayon))
            #
            # painter.drawEllipse(QPointF(sizeTest, rayon), rayon - 2, rayon - 2)
            # line = QLineF(QPointF(0, 0), QPointF(1, 1))
            # line.setP1(QPointF(sizeTest, rayon))
            # line.setAngle(self._angle_vectors[3] * (180 / np.pi))
            # line.setLength(62)
            # painter.drawLine(line)

        # https://stackoverflow.com/questions/16662638/how-to-draw-a-line-at-angle-in-qt


class GuiFourierDraw(QWidget):
    tick = Signal()
    play_pressed = Signal()
    pause_pressed = Signal()
    previous_pressed = Signal()
    next_pressed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.setFixedHeight(700)
        self.setFixedWidth(800)
        __mainLayout = QVBoxLayout()
        __topLayout = QHBoxLayout()
        self.__guiIntervals = GuiFourierDrawIntervals()  #
        # self.__canvas = QLabel()
        # self.__canvas.setPixmap(QPixmap())
        self.__guiControls = GuiFourierDrawControls()  #
        self.__guiControls.play_pressed.connect(self.play_pressed)
        self.__guiControls.pause_pressed.connect(self.pause_pressed)
        self.__guiControls.previous_pressed.connect(self.pressed_previous)
        self.__guiControls.next_pressed.connect(self.pressed_next)
        self.__drawBoard = GuiFourierDrawBoard()  #
        self.__drawBoard.tick.connect(self.tick.emit)
        __topLayout.addWidget(self.__guiIntervals)
        __topLayout.addWidget(self.__drawBoard)
        __mainLayout.addLayout(__topLayout)
        __mainLayout.addWidget(self.__guiControls)
        self.setLayout(__mainLayout)

    def erase_drawing(self):
        self.__drawBoard.stop_sim()
        self.__drawBoard.erase_drawing()

    def reset_drawing(self):
        self.__drawBoard.erase_drawing()

    def start_sim(self, vectors, interval):
        self.__drawBoard.start_sim()
        self.__drawBoard.update_sim(vectors)
        self.__guiIntervals.set_interval(interval)

    def update_sim(self, vectors, interval):
        self.__drawBoard.update_sim(vectors)
        self.__guiIntervals.set_interval(interval)

    def stop_sim(self):
        self.__drawBoard.stop_sim()



    @Slot()
    def pressed_previous(self):
        self.stop_sim()
        self.previous_pressed.emit()

    @Slot()
    def pressed_next(self):
        self.stop_sim()
        self.next_pressed.emit()

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


        self.setFixedHeight(600)
        self.setFixedWidth(700)
        self.path = []
        self.path_result = []
        self.is_drawing = False

        # Insertion des boutons dans les layouts
        self.setLayout(__mainLayout)
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.tick.emit)

    def start_sim(self):
        self.__timer.start(33)

    def stop_sim(self):
        self.__timer.stop()

    def update_sim(self, vectors):
        self.path = vectors
        self.update()

    def erase_drawing(self):
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

    play_pressed = Signal()
    pause_pressed = Signal()
    previous_pressed = Signal()
    next_pressed = Signal()

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
        self.__btnPlayPause.clicked.connect(self.clique_btn_play)
        self.__btnPrevious.clicked.connect(self.previous_pressed)
        self.__btnNext.clicked.connect(self.next_pressed)

        # Insertion des sous-layout dans le main layout
        __mainLayout.addLayout(__topLayout)
        __mainLayout.addLayout(__bottomLayout)
        self.setLayout(__mainLayout)

    def clique_btn_play(self):
        if self.__btnPlayPause.text() == "Play":
            self.__btnPlayPause.setText("Pause")
            self.play_pressed.emit()
            return
        self.__btnPlayPause.setText("Play")
        self.pause_pressed.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("red"))


class GuiFourierDrawIntervals(QWidget):
    """
    BLEU
    """

    interval_changed = Signal(int)

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

    def set_interval(self, interval):
        self.__intervalScroll.setValue(100 - (interval * 100))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("blue"))
