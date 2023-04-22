import math

import numpy as np

from Model.vector_manager import VectorManager
from Model.sketch import Sketch


class Model:
    def __init__(self):
        self.__sketch = Sketch()
        self.precision = 200
        self.nb_vecteurs = 101
        self._vector_manager = VectorManager(10)
        self.set_carre()
        self._vector_manager.start_sim()

    def set_carre(self):
        d = DrawingAnalyzer(self.__sketch.dessinCarre, self.precision)
        array = d.get_intermediary_points()
        vectors = self.fft(array)
        self._vector_manager.matrix_vect = vectors

    def tick(self):
        return self._vector_manager.update()

    def fft(self, coords_list):
        """
        yo
        :param coords_list:
        :return: vectos
        """
        vecteurs = np.zeros((self.nb_vecteurs, 2))
        """
        yo
        """
        index = 0
        # Boucle pour calculer chaque cn
        for i in range(int(self.nb_vecteurs / 2 + 1)):  # dans cas hypo 101 vecteurs
            # Boucle pour avoir les cn positifs et négatif de même chiffre
            for j in range(-1, 2, 2):
                resultat = 0
                if i > 0:
                    index += 1
                # ------------------------------------------------------------------------------------------------------
                # n du cn
                n = i * j  # mettre parties egales dans + et -
                # ------------------------------------------------------------------------------------------------------
                # calcul de l'intervale pour un cn
                for p in range(self.precision):
                    t = p / (self.precision - 1)  # step
                    a, b = coords_list[p][0], coords_list[p][1]
                    exp_cmplx = np.exp((-2 * np.pi) * 1j * n * t)
                    fnc_de_t = (a + b * 1j)  # a + bi
                    resultat += exp_cmplx * fnc_de_t
                    # ------------------------------------------------------------------------------------------------------
                # moyenne
                resultat = resultat / self.precision
                # transformation du cn de la forme cartésienne à la forme polaire
                rayon = math.sqrt((np.imag(resultat) ** 2) + (np.real(resultat) ** 2))
                angle = math.atan2(np.imag(resultat), np.real(resultat))
                if i > 0 or j > 0:
                    vecteurs[index, :] = np.array([rayon, angle])
        return vecteurs

    # def testFFT(self):
    #     print("vector_updates")
    #     self._vector_manager.update_test(0.0)
    #     self._vector_manager.update_test(0.25)
    #     self._vector_manager.update_test(0.5)
    #     self._vector_manager.update_test(0.75)
    #     self._vector_manager.update_test(1.0)


class DrawingAnalyzer:
    def __init__(self, drawing: list, precision):
        self.__drawing = drawing
        self.__precision = precision
        self.__drawingInfo = np.zeros((len(self.__drawing), 5))
        self.__intermediaryPoints = np.zeros((self.__precision, 2))
        self.__longueure_dessin = 0.0
        self.mesurer_lignes()

    def mesurer_lignes(self):
        # ajout premier point
        self.__drawingInfo[0, :] = [self.__drawing[0].x(), self.__drawing[0].y(), 0, 0, 0]
        i = 1
        nb_points = len(self.__drawing)
        distance_abs = 0
        while i < nb_points:
            x1 = self.__drawing[i - 1].x()
            x2 = self.__drawing[i].x()
            y1 = self.__drawing[i - 1].y()
            y2 = self.__drawing[i].y()

            tempx = x2 - x1
            tempy = y2 - y1
            # trouver longueur vecteur
            longueur = math.sqrt(tempx ** 2 + tempy ** 2)
            distance_abs += longueur
            self.__drawingInfo[i, :] = [x2, y2, longueur, distance_abs, 0]
            self.__longueure_dessin += longueur
            i += 1
        self.__drawingInfo[:, 4] = self.__drawingInfo[:, 3] / self.__longueure_dessin

    def get_intermediary_points(self):
        step = 1 / (self.__precision - 1)
        for i in range(self.__precision - 1):
            current_step = step * i
            self.__intermediaryPoints[i, :] = self.interpolate(current_step)
        self.__intermediaryPoints[self.__precision - 1, :] = self.__drawingInfo[-1, 0:2]
        # print("intermediary points")
        # print(self.__intermediaryPoints)
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
