# Nom du fichier: gui_fourier.py
#
# Ce fichier contient les classes servant à créer et gèrer les widgets de la partie droite de l'interface principale,
# où se trouve l'animation des vecteurs tournants de Fourier.
#
# Auteurs: Patrice Gallant et Roberto Nightingale

import math
from copy import deepcopy

import numpy as np
from PySide6.QtCore import Qt, QPointF, QLineF
import PySide6
from PySide6.QtCore import Qt, Signal, Slot, QTimer, QEvent
from PySide6.QtGui import QPainter, QColor, QPen, QFontMetrics, QFont
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QScrollBar, QWidget, QFormLayout,
                               QPushButton, QSizePolicy, QLabel, QScrollArea, QSlider, QFrame)


class GuiFourierMain(QWidget):
    """
    Fenêtre se trouvant à droite. Elle affiche tout ce qui concerne Fourier
    """

    tick = Signal()
    play_pressed = Signal()
    previous_pressed = Signal()
    next_pressed = Signal()
    precision_changed = Signal(int)
    nb_vectors_changed = Signal(int)

    def __init__(self, nb_vecteurs, precision, parent=None):
        super().__init__(parent)
        self.__fourierDraw = None
        self.__vectors = None
        self.init_gui(nb_vecteurs, precision)

    def init_gui(self, nb_vecteurs, precision):
        # Déclaration du layout et des sous-widgets. Les sous-widgets ont leurs propres classes
        __mainLayout = QVBoxLayout()
        self.__vectors = GuiFourierVectors()  #
        self.__scrollArea = QScrollArea()
        self.__scrollArea.setWidget(self.__vectors)
        self.__fourierDraw = GuiFourierDraw(nb_vecteurs, precision)  #
        # Insertion des sous-widgets dans le layout
        __mainLayout.addWidget(self.__scrollArea)
        __mainLayout.addWidget(self.__fourierDraw)
        self.setLayout(__mainLayout)
        self.__fourierDraw.tick.connect(self.tick.emit)
        self.__fourierDraw.play_pressed.connect(self.play_pressed.emit)
        self.__fourierDraw.pause_pressed.connect(self.stop_sim)
        self.__fourierDraw.previous_pressed.connect(self.previous_pressed.emit)
        self.__fourierDraw.next_pressed.connect(self.next_pressed.emit)
        self.__fourierDraw.nb_vectors_changed.connect(self.nb_vectors_changed.emit)
        self.__fourierDraw.precision_changed.connect(self.precision_changed.emit)

    @Slot()
    def update_sim(self, vectors, interval):
        self.__fourierDraw.update_sim(vectors[:, 2:], interval)
        self.__vectors.update_sim(vectors[:, 0:2])

    @Slot()
    def start_sim(self, vectors, interval):
        self.__fourierDraw.start_sim(vectors[:, 2:], interval)
        self.__vectors.update_sim(vectors[:, 0:2])
        self.__scrollArea.ensureVisible(self.__vectors.width() / 2, 0, self.width() / 2, 50)

    @Slot()
    def stop_sim(self):
        self.__fourierDraw.stop_sim()

    @Slot()
    def reset_drawing(self):
        self.__fourierDraw.erase_drawing()

    def erase_drawing(self):
        self.__fourierDraw.erase_drawing()


class GuiFourierVectors(QWidget):
    """
    Vecteurs sur le haut de l'animation qui font le dessin, mais séparés.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_gui()
        self.__angleVectors: np.ndarray = np.zeros(0)

    def init_gui(self):
        self.setLayout(QVBoxLayout())
        self.setFixedHeight(45)

    def update_sim(self, vectors):
        self.__angleVectors = vectors[:61]
        self.__angleVectors = self.__angleVectors[self.__angleVectors[:, 0].argsort()]
        self.setFixedWidth(self.__angleVectors[:, 0].size * 35)  ###
        self.update()

    def paintEvent(self, event):
        __diameterCircle = self.height() - 10
        painter = QPainter(self)

        if self.__angleVectors.size != 0:
            painter.fillRect(self.rect(), QColor("turquoise"))

            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            for i in range(self.__angleVectors[:, 0].size):
                # ref: https://stackoverflow.com/questions/16662638/how-to-draw-a-line-at-angle-in-qt
                painter.drawPoint(QPointF(__diameterCircle / 2 + (i * __diameterCircle), __diameterCircle / 2))
                painter.drawEllipse(QPointF(__diameterCircle / 2 + (i * __diameterCircle), __diameterCircle / 2),
                                    __diameterCircle / 2 - 2, __diameterCircle / 2 - 2)

                line = QLineF(QPointF(0, 0), QPointF(1, 1))
                line.setP1(QPointF(int(__diameterCircle / 2 + (i * __diameterCircle)), __diameterCircle / 2))
                line.setAngle(- self.__angleVectors[i, 1] * (180 / np.pi))
                line.setLength(__diameterCircle / 2 - 2)
                painter.drawLine(line)

                __ecriture = str(int(self.__angleVectors[i, 0]))
                metrics = QFontMetrics(painter.font())
                text_width = metrics.horizontalAdvance(__ecriture)
                painter.drawText(
                    QPointF(int(__diameterCircle / 2 + (i * __diameterCircle) - text_width / 2), self.height()),
                    __ecriture)


class GuiFourierDraw(QFrame):
    tick = Signal()
    play_pressed = Signal()
    pause_pressed = Signal()
    previous_pressed = Signal()
    next_pressed = Signal()
    precision_changed = Signal(int)
    nb_vectors_changed = Signal(int)

    def __init__(self, nb_vecteurs, precision, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        __mainLayout = QVBoxLayout()
        __topLayout = QHBoxLayout()
        self.__guiIntervals = GuiFourierDrawIntervals()
        self.__guiControls = GuiFourierDrawControls(nb_vecteurs, precision)
        self.__guiControls.play_pressed.connect(self.play_pressed.emit)
        self.__guiControls.pause_pressed.connect(self.pause_pressed.emit)
        self.__guiControls.previous_pressed.connect(self.pressed_previous)
        self.__guiControls.next_pressed.connect(self.pressed_next)
        self.__guiControls.precision_changed.connect(self.changed_precision)
        self.__guiControls.nb_vectors_changed.connect(self.changed_nb_vectors)
        self.__drawBoard = GuiFourierDrawBoard()
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
        self.__guiControls.start_sim()
        self.__drawBoard.update_sim(vectors)
        self.__guiIntervals.set_interval(interval)

    def update_sim(self, vectors, interval):
        self.__drawBoard.update_sim(vectors)
        self.__guiIntervals.set_interval(interval)

    def stop_sim(self):
        self.__drawBoard.stop_sim()
        self.__guiControls.stop_sim()

    @Slot()
    def pressed_previous(self):
        self.stop_sim()
        self.previous_pressed.emit()

    @Slot()
    def pressed_next(self):
        self.stop_sim()
        self.next_pressed.emit()

    @Slot()
    def changed_precision(self, precision):
        self.stop_sim()
        self.precision_changed.emit(precision)

    @Slot()
    def changed_nb_vectors(self, nb_vectors):
        self.stop_sim()
        self.nb_vectors_changed.emit(nb_vectors)


class GuiFourierDrawBoard(QWidget):
    """
    S'occupe d'afficher les fleches qui sont attachées pour faire dessin
    """
    tick = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QPushButton {color: black;}")
        self.__timer = None
        self.__isDrawing = None
        self.__pathResult = None
        self.__path = None
        self.__showVect0 = False
        self.init_gui()

    def init_gui(self):
        __mainLayout = QVBoxLayout()
        __infoLayout = QHBoxLayout()
        __infoBtnVectors = QPushButton("?")
        __infoBtnVectors.setFixedWidth(25)
        __infoBtnVectors.setDisabled(True)
        __infoBtnVectors.setToolTip(
            "Une série de Fourier est une décomposition d'une fonction en plus petites parties. "
            "\nJoseph Fourier, le créateur des dites séries, proposait que toute fonction peut"
            "être approximée à partir d'ondes sinus ou cosinus.\nLes lignes tournantes de cette"
            " application représentent chacunes une de ces ondes, et en les mettant l'une après "
            "l'autre, nous pouvons recréer la fonction représentant le dessin.\nCes vecteurs"
            " tournent tous à une vitesse diférente, un nombre différent de tours par intervale.")
        # ref: https://stackoverflow.com/questions/27508552/pyqt-mouse-hovering-on-a-qpushbutton
        __infoBtnVectors.installEventFilter(self)
        self.setFixedHeight(600)
        self.setFixedWidth(700)
        self.__path = []
        self.__pathResult = []
        self.__isDrawing = False

        # Insertion des boutons dans les layouts
        __infoLayout.addStretch()
        __infoLayout.addWidget(__infoBtnVectors)
        __mainLayout.addLayout(__infoLayout)
        __mainLayout.addStretch()
        self.setLayout(__mainLayout)
        self.__timer = QTimer()
        self.__timer.timeout.connect(self.tick.emit)

    def start_sim(self):
        self.__timer.start(33)

    def stop_sim(self):
        self.__timer.stop()

    def update_sim(self, vectors):
        self.__path = vectors
        self.update()

    def erase_drawing(self):
        self.__path = []
        self.__pathResult = []
        self.update()

    # ref: https://stackoverflow.com/questions/27508552/pyqt-mouse-hovering-on-a-qpushbutton
    def eventFilter(self, watched: PySide6.QtCore.QObject, event: PySide6.QtCore.QEvent) -> bool:
        if event.type() == QEvent.HoverEnter:
            self.__showVect0 = True
        if event.type() == QEvent.HoverLeave:
            self.__showVect0 = False
        return False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(255, 255, 255))
        if len(self.__path) <= 0:
            return

        # placer le dernier point dans le dessin
        self.__pathResult.append(deepcopy(self.__path[-1]))

        # recréer le dessin
        painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
        if len(self.__pathResult) > 1:
            for i in range(1, len(self.__pathResult)):
                x1, y1 = self.__pathResult[i - 1][0], self.__pathResult[i - 1][1]
                x2, y2 = self.__pathResult[i][0], self.__pathResult[i][1]
                painter.drawLine(x1, y1, x2, y2)

        # dessin des vecteurs
        if self.__showVect0:
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawLine(0, 0, self.__path[0, 0], self.__path[0, 1])
        for i in range(1, len(self.__path)):
            # vecteurs
            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            painter.drawLine(self.__path[i - 1, 0], self.__path[i - 1, 1], self.__path[i, 0], self.__path[i, 1])

            # cercle autour vecteurs
            painter.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
            __center = QPointF(self.__path[i - 1, 0], self.__path[i - 1, 1])
            __radius = math.sqrt(
                (self.__path[i, 0] - self.__path[i - 1, 0]) ** 2 + (self.__path[i, 1] - self.__path[i - 1, 1]) ** 2)
            painter.drawEllipse(__center, __radius, __radius)


class GuiFourierDrawControls(QFrame):
    play_pressed = Signal()
    pause_pressed = Signal()
    previous_pressed = Signal()
    next_pressed = Signal()
    precision_changed = Signal(int)
    nb_vectors_changed = Signal(int)

    def __init__(self, nb_vectors, precision, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QPushButton {color: black;} QLabel {font-size: 13pt;}")

        # Déclaration des layouts
        __mainLayout = QVBoxLayout()
        __topLayout = QHBoxLayout()
        __bottomLayout = QHBoxLayout()

        # Déclaration des boutons
        self.__labelVectors = QLabel("Nombre de vecteurs: " + str(nb_vectors))
        self.__scrollbarVectors = QSlider(Qt.Horizontal)
        self.__scrollbarVectors.setMinimum(3)
        self.__scrollbarVectors.setMaximum(1001)
        self.__scrollbarVectors.setValue(nb_vectors)
        self.__labelPrecision = QLabel("Précision du dessin: " + str(precision))
        self.__scrollbarPrecision = QSlider(Qt.Horizontal)
        self.__scrollbarPrecision.setValue(precision)
        self.__scrollbarPrecision.setMinimum(10)
        self.__scrollbarPrecision.setMaximum(2001)
        __infoBtnOptions = QPushButton("?")
        __infoBtnOptions.setFixedWidth(25)
        __infoBtnOptions.setDisabled(True)
        __infoBtnOptions.setToolTip("Les lignes tournantes de Fourier sont des vecteurs, qui sont la "
                                    "représentation graphique des coefficients de la série de Fourier. \n"
                                    "Plus il y a de coefficients, plus il y a d'ondes qui, additionnées l'une "
                                    "à l'autre, font une approximation du dessin.\n\n Lorsqu'on analyse un dessin "
                                    "pour trouver sa série de Fourier, il faut le séparer en un nombre de points "
                                    "de distance égale.\n Ces points sont interpretés comme les résultats d'une"
                                    "fonction. La précision indique le nombre de points interpolés, et nous permet"
                                    "de garder plus de détails du dessin durant la transformée de Fourier.")
        self.__btnPrevious = QPushButton("Previous")
        self.__btnPlayPause = QPushButton("Pause")
        self.__btnNext = QPushButton("Next")

        # Insertion des boutons dans les layouts
        __topLayout.addWidget(self.__btnPrevious)
        __topLayout.addWidget(self.__btnPlayPause)
        __topLayout.addWidget(self.__btnNext)
        __bottomLayout.addStretch()
        __bottomLayout.addWidget(__infoBtnOptions)

        # events boutons
        self.__btnPlayPause.clicked.connect(self.clique_btn_play)
        self.__btnPrevious.clicked.connect(self.previous_pressed.emit)
        self.__btnNext.clicked.connect(self.next_pressed.emit)

        # events scrollbars
        self.__scrollbarPrecision.valueChanged.connect(self.change_precision_label_value)
        self.__scrollbarPrecision.sliderReleased.connect(
            lambda: self.precision_changed.emit(self.__scrollbarPrecision.sliderPosition()))
        self.__scrollbarVectors.valueChanged.connect(self.change_vectors_label_value)
        self.__scrollbarVectors.sliderReleased.connect(
            lambda: self.nb_vectors_changed.emit(self.__scrollbarVectors.sliderPosition()))

        # Insertion des sous-layout dans le main layout
        __mainLayout.addLayout(__topLayout)
        __mainLayout.addWidget(self.__labelVectors)
        __mainLayout.addWidget(self.__scrollbarVectors)
        __mainLayout.addWidget(self.__labelPrecision)
        __mainLayout.addWidget(self.__scrollbarPrecision)
        __mainLayout.addLayout(__bottomLayout)
        self.setLayout(__mainLayout)

    def clique_btn_play(self):
        if self.__btnPlayPause.text() == "Play":
            self.__btnPlayPause.setText("Pause")
            self.play_pressed.emit()
            return
        self.__btnPlayPause.setText("Play")
        self.pause_pressed.emit()

    def start_sim(self):
        self.__btnPlayPause.setText("Pause")

    def stop_sim(self):
        self.__btnPlayPause.setText("Play")

    def change_precision_label_value(self, precision):
        self.__labelPrecision.setText("Précision du dessin" + str(precision))

    def change_vectors_label_value(self, nbVectors):
        if nbVectors % 2 == 0:
            nbVectors -= 1
        self.__scrollbarVectors.setValue(nbVectors)
        self.__labelVectors.setText("Nombre de vecteurs: " + str(nbVectors))


class GuiFourierDrawIntervals(QWidget):
    interval_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QPushButton {color: black;}")

        # Déclaration du layout et des boutons
        __mainLayout = QVBoxLayout()
        __infoBtnInterval = QPushButton("?")
        __infoBtnInterval.setFixedWidth(25)
        __infoBtnInterval.setDisabled(True)
        __infoBtnInterval.setToolTip("On calcule une série de Fourier sur une intervale.\n"
                                     "Une intervale est l'ensemble de la fonction entre deux bornes.\n"
                                     "Dans le cas de cette animation, l'intervalle va de 0 à 1.\n"
                                     "Cette barre de défilement représente cette intervalle.")
        self.__intervalScroll = QScrollBar()

        # Insertion des boutons dans le layout
        __mainLayout.addWidget(__infoBtnInterval)
        __mainLayout.addWidget(self.__intervalScroll)
        self.setFixedWidth(60)
        self.setLayout(__mainLayout)

        # progress
        self.__intervalScroll.setRange(0, 1000)
        self.__intervalScroll.setValue(1000)

    def set_interval(self, interval):
        self.__intervalScroll.setValue(1000 - (interval * 1000))
