import math
from copy import deepcopy

import numpy as np
from PySide6.QtCore import Qt, Signal, Slot, QTimer, QPointF, QLineF
import PySide6
from PySide6.QtCore import Qt, Signal, Slot, QTimer, QEvent
from PySide6.QtGui import QPainter, QColor, QPixmap, QPen, QPalette, QFontMetrics, QFont
from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QToolButton, QScrollBar, QWidget, QFormLayout,
                               QPushButton, QSizePolicy, QLabel, QLineEdit, QScrollArea, QSlider, QToolTip, QFrame)


class GuiFourierMain(QWidget):
    """
    JAUNE
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
        self.__fourier_draw = None
        self.__vectors = None
        self.init_gui(nb_vecteurs, precision)

    def init_gui(self, nb_vecteurs, precision):
        # Déclaration du layout et des sous-widgets. Les sous-widgets ont leurs propres classes
        __mainLayout = QVBoxLayout()

        self.__vectors = GuiFourierVectors()  #
        # self.__vectors.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.__scrollArea = QScrollArea()

        # scrollArea.setFixedWidth(self.__vectors.width())
        # scrollArea.setFixedHeight(self.__vectors.height())

        # scrollArea.setBackgroundRole(QPalette.Dark)
        # scrollArea.setWidgetResizable(False)
        self.__scrollArea.setWidget(self.__vectors)
        # self.__vectors.affaire_deg(self.__scrollArea)

        self.__fourier_draw = GuiFourierDraw(nb_vecteurs, precision)  #
        # Insertion des sous-widgets dans le layout
        __mainLayout.addWidget(self.__scrollArea)
        # scrollArea.verticalScrollBar().setMinimum(0)
        # scrollArea.verticalScrollBar().setMaximum(100)
        # scrollArea.verticalScrollBar().setValue(50)
        __mainLayout.addWidget(self.__fourier_draw)
        self.setLayout(__mainLayout)
        self.__fourier_draw.tick.connect(self.tick.emit)
        self.__fourier_draw.play_pressed.connect(self.play_pressed.emit)
        self.__fourier_draw.pause_pressed.connect(self.stop_sim)
        self.__fourier_draw.previous_pressed.connect(self.previous_pressed.emit)
        self.__fourier_draw.next_pressed.connect(self.next_pressed.emit)
        self.__fourier_draw.nb_vectors_changed.connect(self.nb_vectors_changed.emit)
        self.__fourier_draw.precision_changed.connect(self.precision_changed.emit)

    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.fillRect(self.rect(), QColor("yellow"))

    @Slot()
    def update_sim(self, vectors, interval):
        self.__fourier_draw.update_sim(vectors[:, 2:], interval)
        self.__vectors.update_sim(vectors[:, 0:2])

    @Slot()
    def start_sim(self, vectors, interval):
        self.__fourier_draw.start_sim(vectors[:, 2:], interval)
        self.__vectors.update_sim(vectors[:, 0:2])
        self.__scrollArea.ensureVisible(self.__vectors.width() / 2, 0, self.width() / 2, 50)

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
        self.setFixedHeight(45)

    def update_sim(self, vectors):
        self._angle_vectors = vectors[:61]
        self._angle_vectors = self._angle_vectors[self._angle_vectors[:, 0].argsort()]
        self.setFixedWidth(self._angle_vectors[:, 0].size * 35)  ###
        self.update()

    def paintEvent(self, event):
        diameter_circle = self.height() - 10
        painter = QPainter(self)

        if self._angle_vectors.size != 0:
            painter.fillRect(self.rect(), QColor("turquoise"))

            painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
            for i in range(self._angle_vectors[:, 0].size):
                painter.drawPoint(QPointF(diameter_circle / 2 + (i * diameter_circle), diameter_circle / 2))
                painter.drawEllipse(QPointF(diameter_circle / 2 + (i * diameter_circle), diameter_circle / 2),
                                    diameter_circle / 2 - 2, diameter_circle / 2 - 2)

                line = QLineF(QPointF(0, 0), QPointF(1, 1))
                line.setP1(QPointF(int(diameter_circle / 2 + (i * diameter_circle)), diameter_circle / 2))
                line.setAngle(- self._angle_vectors[i, 1] * (180 / np.pi))
                line.setLength(diameter_circle / 2 - 2)
                painter.drawLine(line)

                ecriture = str(int(self._angle_vectors[i, 0]))
                metrics = QFontMetrics(painter.font())
                text_width = metrics.horizontalAdvance(ecriture)
                painter.drawText(
                    QPointF(int(diameter_circle / 2 + (i * diameter_circle) - text_width / 2), self.height()), ecriture)

        # https://stackoverflow.com/questions/16662638/how-to-draw-a-line-at-angle-in-qt

    def affaire_deg(self, scroll: QScrollArea):
        scroll.verticalScrollBar().setValue(50)


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
        # self.setFixedHeight(800)
        # self.setFixedWidth(800)
        __mainLayout = QVBoxLayout()
        __topLayout = QHBoxLayout()
        self.__guiIntervals = GuiFourierDrawIntervals()  #
        # self.__canvas = QLabel()
        # self.__canvas.setPixmap(QPixmap())
        self.__guiControls = GuiFourierDrawControls(nb_vecteurs, precision)  #
        self.__guiControls.play_pressed.connect(self.play_pressed.emit)
        self.__guiControls.pause_pressed.connect(self.pause_pressed.emit)
        self.__guiControls.previous_pressed.connect(self.pressed_previous)
        self.__guiControls.next_pressed.connect(self.pressed_next)
        self.__guiControls.precision_changed.connect(self.changed_precision)
        self.__guiControls.nb_vectors_changed.connect(self.changed_nb_vectors)
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

    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.fillRect(self.rect(), QColor("green"))


class GuiFourierDrawBoard(QWidget):
    """
    Couleur: BLANC
    S'occupe d'afficher les fleches qui sont attachées pour faire dessin
    """
    tick = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QPushButton {color: black;}")
        self.__timer = None
        self.is_drawing = None
        self.path_result = None
        self.path = None
        self.__showVect0 = False
        self.init_gui()

    def init_gui(self):
        __mainLayout = QVBoxLayout()
        __infoLayout = QHBoxLayout()
        __infoBtnVectors = QPushButton("?")
        __infoBtnVectors.setFixedWidth(25)
        __infoBtnVectors.setDisabled(True)
        __infoBtnVectors.setToolTip("Une série de Fourier est une décomposition d'une fonction en plus petites parties. "
                                    "\nJoseph Fourier, le créateur des dites séries, proposait que toute fonction peut"
                                    "être approximée à partir d'ondes sinus ou cosinus.\nLes lignes tournantes de cette"
                                    " application représentent chacunes une de ces ondes, et en les mettant l'une après "
                                    "l'autre, nous pouvons recréer la fonction représentant le dessin.\nCes vecteurs"
                                    " tournent tous à une vitesse diférente, un nombre différent de tours par intervale.")
        #https://stackoverflow.com/questions/27508552/pyqt-mouse-hovering-on-a-qpushbutton
        __infoBtnVectors.installEventFilter(self)
        self.setFixedHeight(600)
        self.setFixedWidth(700)
        self.path = []
        self.path_result = []
        self.is_drawing = False

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
        self.path = vectors
        self.update()

    def erase_drawing(self):
        self.path = []
        self.path_result = []
        self.update()

    def eventFilter(self, watched:PySide6.QtCore.QObject, event:PySide6.QtCore.QEvent) -> bool:
        if event.type() == QEvent.HoverEnter:
            self.__showVect0 = True
        if event.type() == QEvent.HoverLeave:
            self.__showVect0 = False
        return False


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
        if self.__showVect0:
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawLine(0, 0, self.path[0,0], self.path[0,1])
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


class GuiFourierDrawControls(QFrame):
    """
    ROUGE
    """

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
        self.__label_vectors = QLabel("Nombre de vecteurs: " + str(nb_vectors))
        self.__scrollbar_vectors = QSlider(Qt.Horizontal)
        self.__scrollbar_vectors.setMinimum(3)
        self.__scrollbar_vectors.setMaximum(1001)
        self.__scrollbar_vectors.setValue(nb_vectors)
        self.__label_precision = QLabel("Précision du dessin: " + str(precision))
        self.__scrollbar_precision = QSlider(Qt.Horizontal)
        self.__scrollbar_precision.setValue(precision)
        self.__scrollbar_precision.setMinimum(10)
        self.__scrollbar_precision.setMaximum(2001)
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
        self.__scrollbar_precision.valueChanged.connect(self.change_precision_label_value)
        self.__scrollbar_precision.sliderReleased.connect(
            lambda: self.precision_changed.emit(self.__scrollbar_precision.sliderPosition()))
        self.__scrollbar_vectors.valueChanged.connect(self.change_vectors_label_value)
        self.__scrollbar_vectors.sliderReleased.connect(
            lambda: self.nb_vectors_changed.emit(self.__scrollbar_vectors.sliderPosition()))

        # Insertion des sous-layout dans le main layout
        __mainLayout.addLayout(__topLayout)
        __mainLayout.addWidget(self.__label_vectors)
        __mainLayout.addWidget(self.__scrollbar_vectors)
        __mainLayout.addWidget(self.__label_precision)
        __mainLayout.addWidget(self.__scrollbar_precision)
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
        self.__label_precision.setText("Précision du dessin" + str(precision))

    def change_vectors_label_value(self, nb_vectors):
        if nb_vectors % 2 == 0:
            nb_vectors -= 1
        self.__scrollbar_vectors.setValue(nb_vectors)
        self.__label_vectors.setText("Nombre de vecteurs: " + str(nb_vectors))

    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.fillRect(self.rect(), QColor("red"))


class GuiFourierDrawIntervals(QWidget):
    """
    BLEU
    """

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

    def paintEvent(self, event):
        painter = QPainter(self)
        # painter.fillRect(self.rect(), QColor("blue"))
