import math
from PySide6.QtCore import QObject, Signal, Slot
import numpy as np
from vector_manager import VectorManager
from sketch import Sketch
from stack import FStack
from dao import DAO


class Model(QObject):
    sim_updated = Signal(np.ndarray)
    sim_started = Signal(np.ndarray)
    line_removed = Signal(list)
    drawing_deleted = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.precision: int = 2001
        self.nb_vecteurs: int = 1001
        self._vector_manager: VectorManager = VectorManager(10)
        self.__stack = FStack()
        self.__DAO = DAO()
        self.__DAO.connecter()
        self.__DAO.creer_tables()
        self.__DAO.deconnecter()

    @Slot()
    def tick(self):
        self.sim_updated.emit(self._vector_manager.update())

    @property
    def stack(self):
        return self.__stack

    def test_carre(self):
        d = DrawingAnalyzer(Sketch)

    def fft(self, coords_list):
        """
        Fast Fourier Transform
        :param coords_list:
        :return:
        """
        vecteurs = np.zeros((self.nb_vecteurs, 2))
        index = 0
        fncs_de_t = coords_list[:, 0] + coords_list[:, 1] * 1j
        for i in range(math.floor(self.nb_vecteurs / 2 + 1)):  # Boucle pour calculer chaque cn
            for j in range(-1, 2, 2):  # Boucle pour avoir les cn positifs et négatif de même chiffre
                if i > 0:
                    index += 1
                n = i * j  # n du Cn --> multiplication pour inverser -+
                #somme = 0
                ts = np.arange(self.precision * 1.0)
                ts[:] = ts[:] / self.precision
                exp_cmpx = np.exp((-2 * np.pi) * 1j * ts[:] * n)
                somme = np.sum(fncs_de_t[:] * exp_cmpx[:])
                #for p in range(self.precision):  # calcul de l'intervale pour un cn
                    #t = p/self.precision  # step
                    #a, b = coords_list[p, 0], coords_list[p, 1]
                    #ex_cmplx = np.exp((-2 * np.pi) * 1j * n * t)
                    #fnc_de_t = (a + b * 1j)  # a + bi
                    #somme += ex_cmplx * fnc_de_t
                coeff = somme / self.precision  # moyenne des f(t)*e^-2pitn pour former coeff
                # transformation du cn de la forme cartésienne à la forme polaire
                rayon = math.sqrt((np.imag(coeff) ** 2) + (np.real(coeff) ** 2))
                angle = math.atan2(np.imag(coeff), np.real(coeff))
                if i > 0 or j > 0:
                    vecteurs[index, :] = np.array([rayon, angle])
        return vecteurs

    def start_animation(self, drawing):
        d = DrawingAnalyzer(drawing, self.precision)
        array = d.get_intermediary_points()
        vectors = self.fft(array)
        self._vector_manager.matrix_vect = vectors
        self.sim_started.emit(self._vector_manager.start_sim())

    @Slot()
    def receive_line(self, line):
        if len(self.__stack) > 0:
            last_line = self.__stack.pop()
            last_line.pop(-1)
            self.__stack.push(last_line)
        self.__stack.push(line)
        self.start_animation(self.__stack)

    @Slot()
    def undo_line(self):
        if len(self.__stack) > 0:
            self.__stack.pop()
            self.start_animation(self.__stack)
            # self.line_removed.emit(self.__stack.objects)

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
                drawing_data += str(point.x()) + ',' + str(point.y()) + ';'
        self.__DAO.connecter()
        self.__DAO.insert_dessins(drawing_name, drawing_data)
        self.__DAO.deconnecter()

    @Slot()
    def get_all_drawings(self):
        pass

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
        # [[QPointF, QPointF], [QPointF, QPointF, QPointF]]
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
