import numpy as np

from drawing_analyzer import DrawingAnalyzer
from sketch import Sketch


class Model:
    def __init__(self):
        self.__sketch = Sketch()
        self.precision = 6
        self.nb_vecteurs = 100

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

    def fft(self, coord: np.ndarray):
        for i in range(coord):
            np.fft
            print("immigration canada")


if __name__ == "__main__":
    m = Model()
    m.test()
