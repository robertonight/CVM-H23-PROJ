from time import perf_counter
import numpy as np
import math


class VectorManager:
    def __init__(self, max_time: float):
        self._matrix_vect: np.ndarray = None
        self._interval: int = 0
        self._max_time = max_time
        self._last_time = 0.0

    @property
    def matrix_vect(self):
        return self._matrix_vect

    @matrix_vect.setter
    def matrix_vect(self, matrix_coefficients: np.ndarray):  # c'était new matrix avant btw
        temp_matrix = np.zeros((matrix_coefficients[:, 0].size, 5))  # je trouvais que c'était plus clair que len
        temp_matrix[:, 0:2] = matrix_coefficients
        temp_matrix[:, 2] = matrix_coefficients[:, 1]
        self._matrix_vect = temp_matrix

    @property
    def max_time(self):
        return self._max_time

    @max_time.setter
    def max_time(self, max_time: float):
        self._max_time = max_time

    def start_sim(self):
        """
        Cette fonction doit être lancée avant de commencer les updates. C'est elle qui va donner une valeur à
        la variable _last_time. Update ne peut pas marcher si _last_time est None. Si la simulation est redémarrée après
        avoir été arrêtée, il faut appeller à nouveau start_sim, afin de pouvoir remettre la variable _last_time à la
        bonne valeur pour continuer
        :return:
        """
        self._last_time = perf_counter()
        vector_coords = self.update()
        return vector_coords

    def update(self):
        """
        Le elapsed_time est utilisé avec max_time pour obtenir un pourcentage. Puisque l'interval se fait de 0 à 1,
        le pourcentage obtenu peut être additionné pour donner le t de l'interval voulu. Un modulo assure que le
        maximum de l'interval n'est jamais dépassé. Avec l'interval, on mesure le nombre de radians que chaque vecteur
        doit tourner et on l'additionne à leur angle actuel. On obtient ensuite la forme cartésienne des vecteurs,
        et on les additionne les un aux autres afin que leurs coordonnées soient un
        :return:
        """
        current_time = perf_counter()
        elapsed_time = current_time - self._last_time
        self._last_time = current_time  # dans le futur
        self._interval = math.fmod(
            (self._interval + elapsed_time / self.max_time), 1)  # modulo quand tourne + loin que cercle
        n_positifs = np.arange(1, self._matrix_vect[:, 0].size / 2)
        n_negatifs = -1 * n_positifs
        matrice_de_n = np.zeros(self._matrix_vect[:, 0].size, dtype=int)
        matrice_de_n[1::2] = n_positifs
        matrice_de_n[2::2] = n_negatifs
        rad_change = self._interval * 2 * math.pi
        self._matrix_vect[:, 2] = np.fmod((self._matrix_vect[:, 1] + (rad_change * matrice_de_n[:])), (2 * math.pi))
        reel = self._matrix_vect[:, 0] * np.cos(self._matrix_vect[:, 2])
        imag = self._matrix_vect[:, 0] * np.sin(self._matrix_vect[:, 2])
        self._matrix_vect[:, 3] = reel[:]
        self._matrix_vect[:, 4] = imag[:]
#        index = 0
#        for i in range(int(len(self._matrix_vect) / 2 + 1)):
#            for j in range(-1, 2, 2):
#                if i > 0:
#                    index += 1
#                n = i * -j
#                rad_change = self._interval * 2 * math.pi
#                self._matrix_vect[index, 2] = math.fmod((self._matrix_vect[index, 1] + (rad_change * n)), (2 * math.pi))
#                reel = self._matrix_vect[index, 0] * math.cos(self._matrix_vect[index, 2])
#                imag = self._matrix_vect[index, 0] * math.sin(self._matrix_vect[index, 2])
#                self._matrix_vect[index, 3:] = np.array([reel, imag])
        for i in range(1, len(self._matrix_vect)):
            precedent = i - 1
            self._matrix_vect[i, 3:] = self._matrix_vect[i, 3:] + self._matrix_vect[precedent, 3:]
        return self._matrix_vect[:, 2:]
