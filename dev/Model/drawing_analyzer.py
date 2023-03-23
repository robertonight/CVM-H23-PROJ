import math
import numpy as np


class DrawingAnalyzer:
    def __init__(self, drawing: list, precision):
        self.__drawing = drawing
        self.__precision = precision
        self.__drawingInfo = np.zeros((len(self.__drawing), 5))
        self.__intermediaryPoints = np.zeros((self.__precision, 2))
        self.__longueure_dessin = 0.0
        self.mesurer_lignes()

    def mesurer_lignes(self):
        # ajout premier point
        self.__drawingInfo[0, :] = [self.__drawing[0].x(), self.__drawing[0].y(), 0, 0, 0]
        i = 1
        nb_points = len(self.__drawing)
        distance_abs = 0
        while i < nb_points:
            x1 = self.__drawing[i - 1].x()
            x2 = self.__drawing[i].x()
            y1 = self.__drawing[i - 1].y()
            y2 = self.__drawing[i].y()

            tempx = x2 - x1
            tempy = y2 - y1
            # trouver longueur vecteur
            longueur = math.sqrt(tempx ** 2 + tempy ** 2)
            distance_abs += longueur
            self.__drawingInfo[i, :] = [x2, y2, longueur, distance_abs, 0]
            self.__longueure_dessin += longueur
            i += 1
        self.__drawingInfo[:, 4] = self.__drawingInfo[:, 3] / self.__longueure_dessin

    def get_intermediary_points(self):
        step = 1 / (self.__precision - 1)
        for i in range(self.__precision - 1):
            current_step = step * i
            self.__intermediaryPoints[i, :] = self.interpolate(current_step)
        self.__intermediaryPoints[self.__precision - 1, :] = self.__drawingInfo[-1, 0:2]
        return self.__intermediaryPoints

    def interpolate(self, step_ratio):
        i = 0
        if step_ratio != 0:
            i = np.max(np.nonzero(self.__drawingInfo[:, 4] < step_ratio))
        m = self.__drawingInfo[i, 4]
        M = self.__drawingInfo[i + 1, 4]
        r = (step_ratio - m) * (1 / (M - m))
        dx = self.__drawingInfo[i + 1, 0] - self.__drawingInfo[i, 0]
        dy = self.__drawingInfo[i + 1, 1] - self.__drawingInfo[i, 1]
        xp = dx * r + self.__drawingInfo[i, 0]
        yp = dy * r + self.__drawingInfo[i, 1]
        return np.array((xp, yp))
