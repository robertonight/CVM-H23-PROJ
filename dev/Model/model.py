import math

import numpy as np

from drawing_analyzer import DrawingAnalyzer
from vectory_manager import VectorManager
from sketch import Sketch


class Model:
    def __init__(self):
        self.__sketch = Sketch()
        self.precision = 5
        self.nb_vecteurs = 10
        self._vector_manager = VectorManager(10)

    def test(self):
        print("Test carré:")
        print("---------------------------------------------")
        d = DrawingAnalyzer(self.__sketch.dessinCarre, self.precision)
        array = d.get_intermediary_points()
        print(array)

    def testFFT(self):
        d = DrawingAnalyzer(self.__sketch.dessinCarre, self.precision)
        array = d.get_intermediary_points()
        vectors = self.fft(array)
        self._vector_manager.matrmatrix_vect = vectors

    def fft(self, coord):
        vecteurs = np.zeros((self.nb_vecteurs, 3))
        e = np.exp(1)  # euler
        for i in range(self.nb_vecteurs):  # dans cas hypo 101 vect
            resultat = 0
            n = i - int(self.nb_vecteurs / 2)  # mettre parties egales dans + et -
            for p in range(self.precision):
                t = p / (self.precision - 1)  # step
                a, b = coord[p][0], coord[p][1]

                pi2 = -2 * np.pi
                exp = pi2 * 1j * n * t
                coeff = e ** exp

                resultat += (a + b * 1j) * coeff  # a + bi

            nb1 = np.imag(resultat) ** 2
            nb2 = np.real(resultat) ** 2
            temp = nb1 + nb2
            rayon = math.sqrt(temp)
            angle = math.atan2(np.imag(resultat), np.real(resultat))
            vecteurs[i, :] = np.array([n, rayon, angle])
            # vecteurs[i, :] = np.array([n, np.real(resultat), np.imag(resultat)])
        return vecteurs


if __name__ == "__main__":
    m = Model()
    m.testFFT()
