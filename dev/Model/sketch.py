from PySide6.QtCore import QPointF


class Sketch:
    def __init__(self):
        self.__dessinCarre = [QPointF(0.0, 0.0), QPointF(2000.0, 0.0), QPointF(20.0, 2000.0), QPointF(0.0, 2000.0),
                              QPointF(0.0, 0.0)]
        self.__dessinTriangle = [QPointF(0.0, 0.0), QPointF(10.0, 20.0), QPointF(20.0, 0.0), QPointF(0.0, 0.0)]
        self.__dessinPentagone = [QPointF(10.0, 0.0), QPointF(0.0, 10.0), QPointF(20.0, 20.0), QPointF(40.0, 10.0),
                                  QPointF(30.0, 0.0), QPointF(10.0, 0.0)]

    @property
    def dessinCarre(self):
        return self.__dessinCarre

    @property
    def dessinTriangle(self):
        return self.__dessinTriangle

    @property
    def dessinPentagone(self):
        return self.__dessinPentagone
