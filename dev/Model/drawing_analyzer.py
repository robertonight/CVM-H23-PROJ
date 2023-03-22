import math


class DrawingAnalyzer:
    def __init__(self, drawing: list, precision):
        self.__drawing = drawing
        self.__intermediaryPoints = []
        self.__precision = precision
        self.__lineLengths = []
        self.__fullLenght = 0.0
        self.mesurer_lignes()

    def mesurer_lignes(self):
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
        # print("yo")

    def interpolate(self):
        step = self.__fullLenght / self.__precision
        # currentLength = L'emplacement actuel sur tout le dessin. segmentLenght = L'emplacement actuel sur le vecteur
        # courant. indexLength = l'index du vecteur courrant dans la liste de longeurs de vecteurs.
        self.__intermediaryPoints.append((self.__drawing[0].x(), self.__drawing[0].y()))
        currentLenght, segmentLenght = 0, 0
        currentLenght += step
        segmentLenght += step
        if currentLenght > 70:
            print("yeayea")
        indexLenght = 0
        # slope = pente de la droite, origin = ordonée à l'origine de la droite
        slope, origin = self.find_slope_and_origin(indexLenght)
        # On s'assure de ne pas dépasser la longeur du dessin complet
        while currentLenght <= self.__fullLenght:

            # On s'assure de ne pas dépasser la longeur du vecteur courant
            if self.__lineLengths[indexLenght] >= segmentLenght:
                if slope is not None:
                    xp = self.x_p_intermediaire(self.__drawing[indexLenght + 1].x(),
                                                self.__drawing[indexLenght].x(),
                                                self.__lineLengths[indexLenght],
                                                segmentLenght)
                    yp = slope * xp + origin  # y = ax + b
                else:
                    xp = self.__drawing[indexLenght].x()
                    # condition ici --> si on ajoute a segmentLenght a Y et qu'il est plus grand que longueure vect il faut "reculer alors sous-traire"
                    yp = self.__drawing[indexLenght].y() + segmentLenght
                    if self.__drawing[indexLenght].y() > self.__drawing[indexLenght + 1].y():
                        yp = self.__drawing[indexLenght].y() - segmentLenght
                self.__intermediaryPoints.append((xp, yp))
                currentLenght += step
                segmentLenght += step
            else:
                segmentLenght -= self.__lineLengths[indexLenght]
                indexLenght += 1
                slope, origin = self.find_slope_and_origin(indexLenght)
        for point in self.__intermediaryPoints:
            print(f"coordonées: {point[0]}, {point[1]}")

    def find_slope_and_origin(self, i):
        x_1, x_2 = self.__drawing[i].x(), self.__drawing[i + 1].x()
        y_1, y_2 = self.__drawing[i].y(), self.__drawing[i + 1].y()
        try:  # eviter division par 0
            slope = (y_2 - y_1) / (x_2 - x_1)  # a
            origin = y_1 - (slope * x_1)  # b
        except:
            slope, origin = None, None
        return slope, origin

    def x_p_intermediaire(self, x_2, x_1, vector, segmentLenght):
        # On fait le calcul des coordonnées x et y du point intermédiare que l'on recherche

        # je fait etape par etape pour debug

        # print(f"x2:{x_2}")
        # print(f"x1:{x_1}")
        # print(f"segment_length:{segmentLenght}")
        # print(f"vector:{vector}")
        # print((x_2 - x_1) * (segmentLenght / vector))
        # if segmentLenght + vector > vector:
        #     return vector - segmentLenght
        nombre = (x_2 - x_1) * (segmentLenght / vector)
        if nombre < 0:
            nombre += vector

        return nombre
