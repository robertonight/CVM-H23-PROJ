from drawing_analyzer import DrawingAnalyzer
from sketch import Sketch


class Model:
    def __init__(self):
        self.__sketch = Sketch()
        self.precision = 5

    def test(self):
        print("Test carré:")
        print("---------------------------------------------")
        d = DrawingAnalyzer(self.__sketch.dessinCarre, self.precision)
        d.interpolate()
        print("---------------------------------------------")
        print("Test Triangle:")
        print("---------------------------------------------")
        d = DrawingAnalyzer(self.__sketch.dessinTriangle, self.precision)
        d.interpolate()
        print("---------------------------------------------")
        print("Test Pentagone:")
        print("---------------------------------------------")
        d = DrawingAnalyzer(self.__sketch.dessinPentagone, self.precision)
        d.interpolate()


if __name__ == "__main__":
    m = Model()
    m.test()
