import math

import numpy as np

from Model.drawing_analyzer import DrawingAnalyzer
from Model.vectory_manager import VectorManager
from Model.sketch import Sketch


class Model:
    def __init__(self):
        self.__sketch = Sketch()
        self.precision = 50
        self.nb_vecteurs = 10
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

    def testFFT(self):
        d = DrawingAnalyzer(self.__sketch.dessinCarre, self.precision)
        array = d.get_intermediary_points()
        vectors = self.fft(array)
        self._vector_manager.matrix_vect = vectors
        self._vector_manager.update_test(1.0)

    def fft(self, coord):
        vecteurs = np.zeros((self.nb_vecteurs, 2))
        for i in range(int(self.nb_vecteurs / 2)):  # dans cas hypo 101 vecteurs
            for j in range(-1, 2, 2):
                resultat = 0
                n = i * j  # mettre parties egales dans + et -
                for p in range(self.precision):
                    t = p / (self.precision - 1)  # step
                    a, b = coord[p][0], coord[p][1]
                    coeff = np.exp((-2 * np.pi) * 1j * n * t)
                    resultat += (a + b * 1j) * coeff  # a + bi
                resultat = resultat / self.precision
                nb1 = np.imag(resultat) ** 2
                nb2 = np.real(resultat) ** 2
                temp = nb1 + nb2
                rayon = math.sqrt(temp)
                angle = math.atan2(np.imag(resultat), np.real(resultat))
                vecteurs[i, :] = np.array([rayon, angle])
        return vecteurs


if __name__ == "__main__":
    m = Model()
    m.testFFT()
