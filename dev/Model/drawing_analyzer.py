import math


class DrawingAnalyzer:
    def __init__(self, drawing: list, precision):
        self.__drawing = drawing
        self.__intermediaryPoints = []
        self.__precision = precision
        self.__lineLengths = []
        self.__fullLenght = 0.0
        self.mesureLines()
        self.interpolate()

    def mesureLines(self):
        i = 0
        nb_points = (len(self.__drawing) - 1)
        while i < nb_points:
            x1 = self.__drawing[i + 1].x()
            x2 = self.__drawing[i].x()
            y1 = self.__drawing[i + 1].y()
            y2 = self.__drawing[i].y()

            tempx = x1 - x2
            tempy = y1 - y2
            # trouver longueur vecteur
            lineLength = math.sqrt(tempx ** 2 + tempy ** 2)
            self.__lineLengths.append(lineLength)
            self.__fullLenght += lineLength
            i += 1
        print("yo")

    def interpolate(self):
        step = self.__fullLenght / self.__precision
        # mon step represente 1% de la precision que je cherche

        # si full length est 53
        # si precision est 84
        # faut fractionner Grosse longueure en 84

        # 53/84 = 0.6309523809523809

        # 1 step = 0.6309523809523809

        # currentLength = L'emplacement actuel sur tout le dessin. segmentLenght = L'emplacement actuel sur le vecteur
        # courant. indexLength = l'index du vecteur courrant dans la liste de longeurs de vecteurs.
        self.__intermediaryPoints.append((self.__drawing[0].x(), self.__drawing[0].y()))
        currentLenght = 0
        segmentLenght = 0
        currentLenght += step
        segmentLenght += step
        indexLenght = 0
        # slope = la pente du vecteur courrant. origin = l'ordonnée à l'origine du vecteur courrant
        # a = (y2 - y1) / (x2 - x1)
        slope = (self.__drawing[1].y() - self.__drawing[0].y()) / (self.__drawing[1].x() - self.__drawing[0].x())
        # b = y - ax
        origin = self.__drawing[0].y() - (slope * self.__drawing[0].x())
        # On s'assure de ne pas dépasser la longeur du dessin complet
        while currentLenght <= self.__fullLenght:
            # On s'assure de ne pas dépasser la longeur du vecteur courant
            if self.__lineLengths[indexLenght] >= segmentLenght:
                # On fait le calcul des coordonnées x et y du point intermédiare que l'on recherche
                xp = (self.__drawing[indexLenght + 1].x() - self.__drawing[indexLenght].x()) * segmentLenght
                # y = ax + b
                yp = slope * xp + origin
                self.__intermediaryPoints.append((xp, yp))
            else:
                segmentLenght -= self.__lineLengths[indexLenght]
                indexLenght += 1

                temp_x2 = self.__drawing[indexLenght + 1].x()
                temp_x1 = self.__drawing[indexLenght].x()
                temp_y2 = self.__drawing[indexLenght + 1].y()
                temp_y1 = self.__drawing[indexLenght].y()
                slope = (temp_x2 - temp_x1) / (temp_y2 - temp_y1)

                origin = self.__drawing[indexLenght].y() - (slope * self.__drawing[indexLenght].x())
            currentLenght += step
            segmentLenght += step
        for point in self.__intermediaryPoints:
            print(f"coordonées: {point[0]}, {point[1]}")
