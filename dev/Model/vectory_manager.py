from time import time
import numpy as np


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
        temp_matrix = np.zeros(len(new_matrix), 5)
        temp_matrix[:, 0:1] = new_matrix
        temp_matrix[:, 2] = new_matrix[:, 1]
        self._matrix_vect = temp_matrix

    @property
    def max_time(self):
        return self._max_time

    @max_time.setter
    def max_time(self, max_time):
        self._max_time = max_time

    def start_sim(self):
        pass

    def update(self, interval):
        for i in range(len(self._matrix_vect)):
            n = i - int(len(self._matrix_vect) / 2)
            degree_change = interval * 360
            self._matrix_vect[]
