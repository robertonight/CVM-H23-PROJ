# Nom du fichier: model.py
#
# Ce fichier contient le modèle de notre projet, qui est conçu dans un design modèle-vue. Il contient la classe Model
# et la classe DrawingAnalyzer.
#
# Auteurs: Patrice Gallant et Roberto Nightingale


import math
from PySide6.QtCore import QObject, Signal, Slot
import numpy as np
from vector_manager import VectorManager
from utils import FStack
from dao import DAO
from time import perf_counter


class Model(QObject):
    sim_updated = Signal(np.ndarray, float)
    sim_started = Signal(np.ndarray, float)
    drawing_deleted = Signal()
    new_animation_started = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__precision: int = 501
        self.__nbVectors: int = 201
        self.__vectorManager: VectorManager = VectorManager(10)
        self.__stack = FStack()
        self.__matrixN = np.zeros(self.nbVectors, dtype=int)
        self.__DAO = DAO()
        self.__DAO.connecter()
        self.__DAO.creer_tables()
        self.__DAO.deconnecter()

    @property
    def stack(self):
        return self.__stack

    @property
    def nbVectors(self):
        return self.__nbVectors

    @nbVectors.setter
    def nbVectors(self, nbVectors):
        self.__nbVectors = nbVectors

    @property
    def precision(self):
        return self.__precision

    @precision.setter
    def precision(self, precision):
        self.__precision = precision

    @Slot()
    def tick(self):
        __matrixTemp = np.zeros((self.nbVectors, 4))
        __matrixTemp[:, 1:] = self.__vectorManager.update()
        __matrixTemp[:, 0] = self.__matrixN[:]
        self.sim_updated.emit(__matrixTemp, self.__vectorManager.interval)

    def fft(self, coords_list):
        __vectors = np.zeros((self.nbVectors, 2))
        __fncsOfT = coords_list[:, 0] + coords_list[:, 1] * 1j
        __positiveN = np.arange(1, self.nbVectors / 2)
        __negativeN = -1 * __positiveN
        self.__matrixN[1::2] = __positiveN
        self.__matrixN[2::2] = __negativeN
        ts = np.arange(self.__precision * 1.0)
        ts[:] = ts[:] / self.__precision
        __cmpxExp = np.exp((-2 * np.pi) * 1j * np.outer(ts, self.__matrixN))
        __cmpxExp = __cmpxExp.T
        __sumCoeff = np.sum(__fncsOfT[:] * __cmpxExp[:], axis=1)
        __sumCoeff = __sumCoeff / self.__precision

        radius = np.sqrt((np.imag(__sumCoeff[:]) ** 2) + (np.real(__sumCoeff[:]) ** 2))
        angle = np.arctan2(np.imag(__sumCoeff[:]), np.real(__sumCoeff[:]))
        __vectors[:, 0] = radius[:]
        __vectors[:, 1] = angle[:]

        return __vectors

    def start_new_animation(self, drawing):
        self.__vectorManager = VectorManager(10)
        self.__matrixN = np.zeros(self.nbVectors, dtype=int)
        __d = DrawingAnalyzer(drawing, self.__precision)
        __array = __d.get_intermediary_points()
        __vectors = self.fft(__array)
        self.__vectorManager.matrix_vect = __vectors
        self.__vectorManager.interval = 0
        self.new_animation_started.emit()
        self.start_sim()

    @Slot()
    def stop_sim(self):
        self.__stack.clear()
        self.__vectorManager.interval = 0

    @Slot()
    def start_sim(self):
        __tempMatrix = np.zeros((self.nbVectors, 4))
        __tempMatrix[:, 1:] = self.__vectorManager.start_sim()
        __tempMatrix[:, 0] = self.__matrixN[:]
        self.sim_started.emit(__tempMatrix, self.__vectorManager.interval)

    @Slot()
    def previous_interval(self):
        self.__vectorManager.interval += -0.005
        self.__vectorManager.last_time = perf_counter()
        self.tick()

    @Slot()
    def next_interval(self):
        self.__vectorManager.interval += 0.005
        self.__vectorManager.last_time = perf_counter()
        self.tick()

    @Slot()
    def receive_line(self, line):
        if len(self.__stack) > 0:
            __lastLine = self.__stack.pop()
            __lastLine.pop(-1)
            self.__stack.push(__lastLine)
        self.__stack.push(line)
        self.start_new_animation(self.__stack)

    @Slot()
    def undo_line(self):
        if len(self.__stack) == 1:
            self.erase_drawing()
            self.__stack.clear()
        elif len(self.__stack) > 0:
            __removedLine = self.__stack.pop()
            __lastLine = self.__stack.pop()
            __lastLine.append(__removedLine.pop(-1))
            self.__stack.push(__lastLine)
            self.start_new_animation(self.__stack)

    @Slot()
    def erase_drawing(self):
        if not self.__stack.is_empty():
            self.__stack.clear()
            self.drawing_deleted.emit()

    @Slot()
    def save_drawing(self, drawing_name):
        __drawing = self.__stack.objects
        __drawingData = ''
        for line in __drawing:
            for point in line:
                __drawingData += str(point.x()) + ' ' + str(point.y()) + ';'
            __drawingData += ':'
        self.__DAO.connecter()
        self.__DAO.insert_dessins(drawing_name, __drawingData)
        self.__DAO.deconnecter()

    def set_drawing(self, drawing):
        self.__stack.clear()
        for line in drawing:
            self.__stack.push(line)
        self.start_new_animation(self.__stack)

    @Slot()
    def change_precision(self, precision):
        self.__precision = precision
        self.start_new_animation(self.__stack)

    @Slot()
    def change_nb_vecteurs(self, nbVectors):
        self.__nbVectors = nbVectors
        self.start_new_animation(self.__stack)

    def get_drawings(self):
        """
        les colonnes dans __drawingsDB sont:
        0: le id du dessin dans la database(inutile)
        1: le nom du dessin
        2: les points du dessin en forme de string. Il est reconverti dans une autre fonction
        3: la date où le dessin à été enregistrée
        :return:
        """
        self.__DAO.connecter()
        __drawingsDB = self.__DAO.select_dessins()
        self.__DAO.deconnecter()
        return __drawingsDB


class DrawingAnalyzer:
    """
    Cette classe sers à décortiquer tous les vecteurs qui constituent le grand dessin continu.
    """

    def __init__(self, drawing: FStack, precision: int):
        """
        :param drawing: liste de tous les QPointF qui constituent le dessin
        :param precision: précision en nombre de parts égales
        """
        # declarations
        __nbPoints = 0
        for line in drawing.objects:  # calculer nb de points
            __nbPoints += len(line)  # nb de points qui se trouvent dans la ligne
        self.__drawing_info: np.ndarray = np.zeros((__nbPoints, 5))
        """ Contient la matrice de 5 infos """
        self.__d: list = drawing.objects
        """ Dessin constitué de :list 2D de paths """
        self.__precision: int = precision
        self.__intermediaryPoints: np.ndarray = np.zeros((precision, 2))
        """
        couple de points decoupes
        """
        self.__drawingLength: float = 0.0

        # ca part
        self.analyzer()

    def analyzer(self):
        """
        cette methode rempli le ndarray(n ,4) __drawingInfo -->
        [[(x), (y), (longueure segment), (longueur absolue), (pourcentage dessin à endroit)],...]
        calcul longuieure de seg entre les points
        """
        self.__drawing_info[0, :] = [self.__d[0][0].x(), self.__d[0][0].y(), 0, 0, 0]  # 1e p.
        idx = 1
        for i in range(len(self.__d)):
            row1, row2 = self.__d[i - 1], self.__d[i]
            if i > 0:
                self.line_analyzer(row1[-1], row2[0], idx)
                idx += 1
            for j in range(1, len(row2)):
                self.line_analyzer(row2[j - 1], row2[j], idx)
                idx += 1
        # --
        self.__drawing_info[:, 4] = self.__drawing_info[:, 3] / self.__drawingLength  # % du dessin à ce point

    def line_analyzer(self, point1, point2, idx):
        __length = math.sqrt((point2.x() - point1.x()) ** 2 + (point2.y() - point1.y()) ** 2)  # trouver long. vecteur
        self.__drawingLength += __length
        self.__drawing_info[idx, :] = [point2.x(), point2.y(), __length, self.__drawingLength, 0]

    def get_intermediary_points(self) -> np.ndarray:  # basically get les t
        __step: float = 1 / self.__precision
        for i in range(self.__precision):
            __currentStep = __step * i
            self.__intermediaryPoints[i, :] = self.interpolate(__currentStep)  # trouve points
        return self.__intermediaryPoints

    def interpolate(self, step_ratio) -> np.ndarray:
        # La fonction interpolate est basée sur une formule que notre professeur nous a enseigné. Les variables sont
        # nommées à partir de cette formule.
        i = 0
        if step_ratio != 0:
            i = np.max(np.nonzero(self.__drawing_info[:, 4] < step_ratio))  # prends + haute longueure
        m = self.__drawing_info[i, 4]
        M = self.__drawing_info[i + 1, 4]
        r = (step_ratio - m) * (1 / (M - m))
        dx = self.__drawing_info[i + 1, 0] - self.__drawing_info[i, 0]
        dy = self.__drawing_info[i + 1, 1] - self.__drawing_info[i, 1]
        xp = dx * r + self.__drawing_info[i, 0]
        yp = dy * r + self.__drawing_info[i, 1]
        return np.array((xp, yp))
