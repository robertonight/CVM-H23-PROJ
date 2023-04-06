from PySide6.QtCore import Signal


class FVect:
    vector_rotated = Signal(object)

    def __init__(self, parent, i):
        self._manager = parent
        self._vect_index = i

    def rotate_vect(self, interval):
        pass
