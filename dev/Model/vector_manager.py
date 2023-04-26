from time import perf_counter
import numpy as np
import math


class VectorManager:
    def __init__(self, max_time):
        self._matrix_vect: np.ndarray = None
        self._interval: int = 0
        self._max_time = max_time
        self._last_time = None

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
    def max_time(self, max_time):
        self._max_time = max_time

    def start_sim(self):
        self._last_time = perf_counter()
        vector_coords = self.update()
        return vector_coords

    def update(self):
        current_time = perf_counter()
        elapsed_time = current_time - self._last_time
        self._last_time = current_time  # dans le futur
        self._interval = math.fmod(
            (self._interval + elapsed_time / self.max_time), 1)  # modulo quand tourne + loin que cercle
        index = 0
        for i in range(int(len(self._matrix_vect) / 2 + 1)):
            for j in range(-1, 2, 2):
                if i > 0:
                    index += 1
                n = i * -j
                rad_change = self._interval * 2 * math.pi
                self._matrix_vect[index, 2] = math.fmod((self._matrix_vect[index, 1] + (rad_change * n)), (2 * math.pi))
                reel = self._matrix_vect[index, 0] * math.cos(self._matrix_vect[index, 2])
                imag = self._matrix_vect[index, 0] * math.sin(self._matrix_vect[index, 2])
                self._matrix_vect[index, 3:] = np.array([reel, imag])
        for i in range(1, len(self._matrix_vect)):
            precedent = i - 1
            self._matrix_vect[i, 3:] = self._matrix_vect[i, 3:] + self._matrix_vect[precedent, 3:]
        return self._matrix_vect[:, 3:]
