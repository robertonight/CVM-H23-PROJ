import math
from PySide6.QtCore import QObject, Signal, Slot
import numpy as np
from vector_manager import VectorManager
from sketch import Sketch
from stack import FStack
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
        self.__nb_vecteurs: int = 201
        self._vector_manager: VectorManager = VectorManager(10)
        self.__stack = FStack()
        self.__matrice_de_n = np.zeros(self.nb_vecteurs, dtype=int)
        self.__DAO = DAO()
        self.__DAO.connecter()
        self.__DAO.creer_tables()
        self.__DAO.deconnecter()

    @property
    def stack(self):
        return self.__stack

    @property
    def nb_vecteurs(self):
        return self.__nb_vecteurs

    @nb_vecteurs.setter
    def nb_vecteurs(self, nb_vecteurs):
        self.__nb_vecteurs = nb_vecteurs

    @property
    def precision(self):
        return self.__precision

    @precision.setter
    def precision(self, precision):
        self.__precision = precision

    @Slot()
    def tick(self):
        temp_matrice = np.zeros((self.nb_vecteurs, 4))
        temp_matrice[:, 1:] = self._vector_manager.update()
        temp_matrice[:, 0] = self.__matrice_de_n[:]
        self.sim_updated.emit(temp_matrice, self._vector_manager.interval)

    def fft(self, coords_list):
        """
        Fast Fourier Transform
        :param coords_list:
        :return:
        """
        vecteurs = np.zeros((self.nb_vecteurs, 2))
        fncs_de_t = coords_list[:, 0] + coords_list[:, 1] * 1j
        n_positifs = np.arange(1, self.nb_vecteurs / 2)
        n_negatifs = -1 * n_positifs
        self.__matrice_de_n[1::2] = n_positifs
        self.__matrice_de_n[2::2] = n_negatifs
        ts = np.arange(self.__precision * 1.0)
        ts[:] = ts[:] / self.__precision
        exp_cmpx = np.exp((-2 * np.pi) * 1j * np.outer(ts, self.__matrice_de_n))
        exp_cmpx = exp_cmpx.T
        somme = np.sum(fncs_de_t[:] * exp_cmpx[:], axis=1)
        somme = somme / self.__precision
        
        rayon = np.sqrt((np.imag(somme[:]) ** 2) + (np.real(somme[:]) ** 2))
        angle = np.arctan2(np.imag(somme[:]), np.real(somme[:]))
        vecteurs[:, 0] = rayon[:]
        vecteurs[:, 1] = angle[:]

        return vecteurs


    def start_new_animation(self, drawing):
        self._vector_manager = VectorManager(10)
        self.__matrice_de_n = np.zeros(self.nb_vecteurs, dtype=int)
        d = DrawingAnalyzer(drawing, self.__precision)
        array = d.get_intermediary_points()
        vectors = self.fft(array)
        self._vector_manager.matrix_vect = vectors
        self._vector_manager.interval = 0
        self.new_animation_started.emit()
        self.start_sim()

    @Slot()
    def stop_sim(self):
        self.__stack.clear()
        self._vector_manager.interval = 0

    @Slot()
    def start_sim(self):
        temp_matrice = np.zeros((self.nb_vecteurs, 4))
        temp_matrice[:, 1:] = self._vector_manager.start_sim()
        temp_matrice[:, 0] = self.__matrice_de_n[:]
        self.sim_started.emit(temp_matrice, self._vector_manager.interval)

    @Slot()
    def previous_interval(self):
        self._vector_manager.interval += -0.005
        self._vector_manager.last_time = perf_counter()
        self.tick()

    @Slot()
    def next_interval(self):
        self._vector_manager.interval += 0.005
        self._vector_manager.last_time = perf_counter()
        self.tick()

    @Slot()
    def receive_line(self, line):
        if len(self.__stack) > 0:
            last_line = self.__stack.pop()
            last_line.pop(-1)
            self.__stack.push(last_line)
        self.__stack.push(line)
        self.start_new_animation(self.__stack)

    @Slot()
    def undo_line(self):
        if len(self.__stack) == 1:
            self.erase_drawing()
            self.__stack.clear()
        elif len(self.__stack) > 0:
            last_line = self.__stack.pop()
            self.__stack.push([last_line.pop(-1)])
            self.start_new_animation(self.__stack)

    @Slot()
    def erase_drawing(self):
        if not self.__stack.is_empty():
            self.__stack.clear()
            self.drawing_deleted.emit()

    @Slot()
    def save_drawing(self, drawing_name):
        drawing = self.__stack.objects
        drawing_data = ''
        for line in drawing:
            for point in line:
                drawing_data += str(point.x()) + ' ' + str(point.y()) + ';'
            drawing_data += ':'
        self.__DAO.connecter()
        self.__DAO.insert_dessins(drawing_name, drawing_data)
        self.__DAO.deconnecter()

    @Slot()
    def change_precision(self, precision):
        self.__precision = precision
        self.start_new_animation(self.__stack)

    @Slot()
    def change_nb_vecteurs(self, nb_vecteurs):
        self.__nb_vecteurs = nb_vecteurs
        self.start_new_animation(self.__stack)

    def get_all_drawings(self):
        """
        les colonnes dans dessins_db sont:
        0: le id du dessin dans la database(inutile)
        1: le nom du dessin
        2: les points du dessin en forme de string. Il est reconverti dans une autre fonction
        3: la date où le dessin à été enregistrée
        :return:
        """
        self.__DAO.connecter()
        dessins_db = self.__DAO.select_dessins()
        self.__DAO.deconnecter()
        return dessins_db

    def get_drawing(self):
        pass


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
        nb_points = 0
        for line in drawing.objects:  # calculer nb de points
            nb_points += len(line)  # nb de points qui se trouvent dans la ligne
        self.__drawing_info: np.ndarray = np.zeros((nb_points, 5))
        """ Contient la matrice de 5 infos """
        self.__d: list = drawing.objects
        """ Dessin constitué de :list 2D de paths """
        self.__precision: int = precision
        self.__intermediary_points: np.ndarray = np.zeros((precision, 2))
        """
        couple de points decoupes
        """
        self.__longueure_dessin: float = 0.0

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
        self.__drawing_info[:, 4] = self.__drawing_info[:, 3] / self.__longueure_dessin  # % du dessin à ce point

    def line_analyzer(self, point1, point2, idx):
        longueur = math.sqrt((point2.x() - point1.x()) ** 2 + (point2.y() - point1.y()) ** 2)  # trouver long. vecteur
        self.__longueure_dessin += longueur
        self.__drawing_info[idx, :] = [point2.x(), point2.y(), longueur, self.__longueure_dessin, 0]

    def get_intermediary_points(self) -> np.ndarray:  # basically get les t
        step: float = 1 / self.__precision
        for i in range(self.__precision):
            current_step = step * i
            self.__intermediary_points[i, :] = self.interpolate(current_step)  # trouve points
        return self.__intermediary_points

    def interpolate(self, step_ratio) -> np.ndarray:
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
