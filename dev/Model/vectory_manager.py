from time import time
import numpy as np
import math


class VectorManager:
    def __init__(self, max_time):
        self._matrix_vect = None
        self._interval = 0
        self._max_time = max_time
        self.start_time = None

    @property
    def matrix_vect(self):
        return self._matrix_vect

    @matrix_vect.setter
    def matrix_vect(self, new_matrix):
        temp_matrix = np.zeros((len(new_matrix), 5))
        temp_matrix[:, 0:2] = new_matrix
        temp_matrix[:, 2] = new_matrix[:, 1]
        self._matrix_vect = temp_matrix

    @property
    def max_time(self):
        return self._max_time

    @max_time.setter
    def max_time(self, max_time):
        self._max_time = max_time

    def start_sim(self):
        self._start_time = time()
        vector_coords = self.update()
        return vector_coords

    def update_test(self, interval):
        for i in range(len(self._matrix_vect)):
            n = i - int(len(self._matrix_vect) / 2)
            degree_change = interval * 2 * math.pi
            self._matrix_vect[i, 2] = math.fmod((self._matrix_vect[i, 1] + degree_change * n), (2*math.pi))
            reel = self._matrix_vect[i, 0] * math.cos(self._matrix_vect[i, 2])
            imag = self._matrix_vect[i, 0] * math.sin(self._matrix_vect[i, 2])
            self._matrix_vect[i, 3:] = np.array([reel, imag])
        for i in range(1, len(self._matrix_vect)):
            precedent = i - 1
            self._matrix_vect[i, 3:] = self._matrix_vect[i, 3:] + self._matrix_vect[precedent, 3:]
        print(self._matrix_vect[-1, 3:])

    def update(self):
        curr_time = time()
        elapsed_time = curr_time - self._start_time
        for i in range(len(self._matrix_vect)):
            n = i - int(len(self._matrix_vect) / 2)
            degree_change = self._interval * 2 * math.pi
            self._matrix_vect[i, 2] = math.fmod((self._matrix_vect[i, 1] + degree_change * n), (2*math.pi))
            reel = self._matrix_vect[i, 0] * math.cos(self._matrix_vect[i, 2])
            imag = self._matrix_vect[i, 0] * math.sin(self._matrix_vect[i, 2])
            self._matrix_vect[i, 3:] = np.array([reel, imag])
        for i in range(1, len(self._matrix_vect)):
            precedent = i - 1
            self._matrix_vect[i, 3:] = self._matrix_vect[i, 3:] + self._matrix_vect[precedent, 3:]
        return self._matrix_vect[:, 3:]