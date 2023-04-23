import math

import numpy as np

from Model.vector_manager import VectorManager
from Model.sketch import Sketch


class Model:
    def __init__(self):
        self.precision: int = 1000
        self.nb_vecteurs: int = 101
        self._vector_manager: VectorManager = VectorManager(10)
        self.tests_formes_sketch()
        self._vector_manager.start_sim()

    def tick(self):
        return self._vector_manager.update()

    def fft(self, coords_list):
        """
        Fast Fourier Transform
        :param coords_list:
        :return:
        """
        vecteurs = np.zeros((self.nb_vecteurs, 2))
        index = 0
        for i in range(math.floor(self.nb_vecteurs / 2 + 1)):  # Boucle pour calculer chaque cn
            for j in range(-1, 2, 2):  # Boucle pour avoir les cn positifs et négatif de même chiffre
                if i > 0:
                    index += 1
                n = i * j  # n du Cn --> multiplication pour inverser -+
                somme = 0
                for p in range(self.precision):  # calcul de l'intervale pour un cn
                    t = p / (self.precision - 1)  # step
                    a, b = coords_list[p][0], coords_list[p][1]
                    ex_cmplx = np.exp((-2 * np.pi) * 1j * n * t)
                    fnc_de_t = (a + b * 1j)  # a + bi
                    somme += ex_cmplx * fnc_de_t
                coeff = somme / self.precision  # moyenne des f(t)*e^-2pitn pour former coeff
                # transformation du cn de la forme cartésienne à la forme polaire
                rayon = math.sqrt((np.imag(coeff) ** 2) + (np.real(coeff) ** 2))
                angle = math.atan2(np.imag(coeff), np.real(coeff))
                if i > 0 or j > 0:
                    vecteurs[index, :] = np.array([rayon, angle])
        return vecteurs

    def tests_formes_sketch(self): # set_carre
        """
        Avec cette methode, on teste les formes préfaites par la classe sketch
        """
        sketch = Sketch()
        d = DrawingAnalyzer(sketch.dessinCarre, self.precision)
        array = d.get_intermediary_points()
        vectors = self.fft(array)
        self._vector_manager.matrix_vect = vectors

    # def testFFT(self):
    #     print("vector_updates")
    #     self._vector_manager.update_test(0.0)
    #     self._vector_manager.update_test(0.25)
    #     self._vector_manager.update_test(0.5)
    #     self._vector_manager.update_test(0.75)
    #     self._vector_manager.update_test(1.0)


class DrawingAnalyzer:
    """
    Cette classe sers à décortiquer tous les vecteurs qui constituent le grand dessin continu.
    """

    def __init__(self, drawing: list, precision: int):
        """
        :param drawing: liste de tous les QPointF qui constituent le dessin
        :param precision: précision en nombre de parts égales
        """
        self.__drawing: list = drawing
        self.__precision: int = precision
        nb_points = 0
        for line in self.__drawing:
            nb_points += len(line)
        self.__drawingInfo: np.ndarray = np.zeros((nb_points, 5))
        self.__intermediaryPoints: np.ndarray = np.zeros((self.__precision, 2))
        self.__longueure_dessin: float = 0.0
        self.mesurer_lignes()

    def mesurer_lignes1(self):
        """
        cette methode rempli le ndarray(n ,4) __drawingInfo -->
        [[(x), (y), (longueure segment), (longueur depuis debut), (jusqu'au segment), (pourcentage dessin à endroit)],...]
        """
        self.__drawingInfo[0, :] = [self.__drawing[0][0].x(), self.__drawing[0][0].y(), 0, 0, 0]  # ajout premier point
        distance_abs = 0
        for i in range(1, len(self.__drawing)):
            x1, x2 = self.__drawing[i - 1].x(), self.__drawing[i].x()
            y1, y2 = self.__drawing[i - 1].y(), self.__drawing[i].y()
            longueur = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # trouver longueur vecteur
            distance_abs += longueur
            self.__drawingInfo[i, :] = [x2, y2, longueur, distance_abs, 0]
            self.__longueure_dessin += longueur
        self.__drawingInfo[:, 4] = self.__drawingInfo[:, 3] / self.__longueure_dessin  # % du dessin à ce point

    def mesurer_lignes(self):
        """
        cette methode rempli le ndarray(n ,4) __drawingInfo -->
        [[(x), (y), (longueure segment), (longueur depuis debut), (jusqu'au segment), (pourcentage dessin à endroit)],...]
        """
        self.__drawingInfo[0, :] = [self.__drawing[0][0].x(), self.__drawing[0][0].y(), 0, 0,
                                    0]  # ajout premier point
        distance_abs = 0
        for line in self.__drawing:
            for i in range(1, len(line)):
                x1, x2 = line[i - 1].x(), line[i].x()
                y1, y2 = line[i - 1].y(), line[i].y()
                longueur = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)  # trouver longueur vecteur
                distance_abs += longueur
                self.__drawingInfo[i, :] = [x2, y2, longueur, distance_abs, 0]
                self.__longueure_dessin += longueur
        self.__drawingInfo[:, 4] = self.__drawingInfo[:, 3] / self.__longueure_dessin  # % du dessin à ce point

    def get_intermediary_points(self):
        step: float = 1 / (self.__precision - 1)
        for i in range(self.__precision - 1):
            current_step = step * i
            self.__intermediaryPoints[i, :] = self.interpolate(current_step)
        self.__intermediaryPoints[self.__precision - 1, :] = self.__drawingInfo[-1, 0:2]
        return self.__intermediaryPoints

    def interpolate(self, step_ratio):
        i = 0
        if step_ratio != 0:
            i = np.max(np.nonzero(self.__drawingInfo[:, 4] < step_ratio))
        m = self.__drawingInfo[i, 4]
        M = self.__drawingInfo[i + 1, 4]
        r = (step_ratio - m) * (1 / (M - m))
        dx = self.__drawingInfo[i + 1, 0] - self.__drawingInfo[i, 0]
        dy = self.__drawingInfo[i + 1, 1] - self.__drawingInfo[i, 1]
        xp = dx * r + self.__drawingInfo[i, 0]
        yp = dy * r + self.__drawingInfo[i, 1]
        return np.array((xp, yp))


if __name__ == "__main__":
    m = Model()
    m.testFFT()
