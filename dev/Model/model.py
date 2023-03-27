import math

import numpy as np

from drawing_analyzer import DrawingAnalyzer
from sketch import Sketch


class Model:
    def __init__(self):
        self.__sketch = Sketch()
        self.precision = 5
        self.nb_vecteurs = 10

    def test(self):
        print("Test carré:")
        print("---------------------------------------------")
        d = DrawingAnalyzer(self.__sketch.dessinCarre, self.precision)
        array = d.get_intermediary_points()
        print(array)

    def testFFT(self):
        d = DrawingAnalyzer(self.__sketch.dessinCarre, self.precision)
        array = d.get_intermediary_points()
        self.fft(array)
        a = np.fft.fft(array, 10)
        print(f"voici fft: {a}")

    def fft(self, coord):
        vecteurs = []
        e = np.exp(1)  # euler
        for i in range(self.nb_vecteurs):  # dans cas hypo 101 vect
            resultat = 0
            n = i - int(self.nb_vecteurs / 2)  # mettre parties egales dans + et -
            for p in range(self.precision):
                t = p / (self.precision - 1)  # step
                a, b = coord[p][0], coord[p][1]
                coeff = e ** ((-n * (2 * np.pi) * 1j) * t)
                resultat += (a + b * 1j) * coeff  # a + bi
            #rayon = math.sqrt(np.real(resultat) ** 2 + np.imag(resultat) ** 2)
            #angle = math.atan2(np.imag(resultat), np.real(resultat))
            #vecteurs.append([rayon, angle])
            vecteurs.append([np.real(resultat), np.imag(resultat)])
        for row in vecteurs:
            print(row)


if __name__ == "__main__":
    m = Model()
    m.testFFT()
