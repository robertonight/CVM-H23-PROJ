from Model.fvect import FVect


class VectorManager:
    def __init__(self, matrix_vect):
        self._matrix_vect = matrix_vect
        self._list_fvect = []
        self._interval = 0
        self._pause = False
        for i in range(len(self._matrix_vect)):
            self._list_fvect.append(FVect(self, i))

    def run_simulation(self):
        while not self._pause:
            pass
