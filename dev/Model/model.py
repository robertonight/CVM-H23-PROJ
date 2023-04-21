import math

import numpy as np

from Model.drawing_analyzer import DrawingAnalyzer
from Model.vectory_manager import VectorManager
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

    def testFFT(self):
        print("vector_updates")
        self._vector_manager.update_test(0.0)
        self._vector_manager.update_test(0.25)
        self._vector_manager.update_test(0.5)
        self._vector_manager.update_test(0.75)
        self._vector_manager.update_test(1.0)

    def fft(self, coords_list):
        vecteurs = np.zeros((self.nb_vecteurs, 2))
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


if __name__ == "__main__":
    m = Model()
    m.testFFT()
