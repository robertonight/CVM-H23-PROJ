# Nom du fichier: vector_manager.py
#
# Ce fichier contient la classe vectorManager, celle-ci prend en paramètres la durée de l'animation et fait la gestion
# de l'affichage de tous les vecteurs.
#
# Auteurs: Roberto Nightingale Castillo et Patrice Gallant

from time import perf_counter
import numpy as np
import math


class VectorManager:
    def __init__(self, max_time: float):
        self.__matrixVect: np.ndarray = None
        self.__interval: int = 0
        self.__maxTime = max_time
        self.__lastTime = 0.0

    @property
    def matrix_vect(self):
        return self.__matrixVect

    @property
    def interval(self):
        return self.__interval

    @interval.setter
    def interval(self, interval: int):
        self.__interval = interval

    @property
    def last_time(self):
        return self.__lastTime

    @last_time.setter
    def last_time(self, time):
        self.__lastTime = time

    @matrix_vect.setter
    def matrix_vect(self, matrixCoeffs: np.ndarray):  # c'était new matrix avant btw
        tempMatrix = np.zeros((matrixCoeffs[:, 0].size, 5))  # je trouvais que c'était plus clair que len
        tempMatrix[:, 0:2] = matrixCoeffs
        tempMatrix[:, 2] = matrixCoeffs[:, 1]
        self.__matrixVect = tempMatrix

    @property
    def max_time(self):
        return self.__maxTime

    @max_time.setter
    def max_time(self, maxTime: float):
        self.__maxTime = maxTime

    def start_sim(self):
        """
        Cette fonction doit être lancée avant de commencer les updates. C'est elle qui va donner une valeur à
        la variable _last_time. Update ne peut pas marcher si _last_time est None. Si la simulation est redémarrée après
        avoir été arrêtée, il faut appeller à nouveau start_sim, afin de pouvoir remettre la variable _last_time à la
        bonne valeur pour continuer
        :return:
        """
        self.__lastTime = perf_counter()
        vectorCoords = self.update()
        return vectorCoords

    def update(self):
        """
        Le elapsedTime est utilisé avec max_time pour obtenir un pourcentage. Puisque l'interval se fait de 0 à 1,
        le pourcentage obtenu peut être additionné pour donner le t de l'interval voulu. Un modulo assure que le
        maximum de l'interval n'est jamais dépassé. Avec l'interval, on mesure le nombre de radians que chaque vecteur
        doit tourner et on l'additionne à leur angle actuel. On obtient ensuite la forme cartésienne des vecteurs,
        et on les additionne les un aux autres afin que leurs coordonnées soient un
        :return:
        """
        currentTime = perf_counter()
        elapsedTime = currentTime - self.__lastTime
        self.__lastTime = currentTime
        self.__interval = math.fmod(
            (self.__interval + elapsedTime / self.max_time), 1)
        positiveN = np.arange(1, self.__matrixVect[:, 0].size / 2)
        negativeN = -1 * positiveN
        matrixN = np.zeros(self.__matrixVect[:, 0].size, dtype=int)
        matrixN[1::2] = positiveN
        matrixN[2::2] = negativeN
        radChange = self.__interval * 2 * math.pi
        self.__matrixVect[:, 2] = np.fmod((self.__matrixVect[:, 1] + (radChange * matrixN[:])), (2 * math.pi))
        real = self.__matrixVect[:, 0] * np.cos(self.__matrixVect[:, 2])
        imag = self.__matrixVect[:, 0] * np.sin(self.__matrixVect[:, 2])
        self.__matrixVect[:, 3] = real[:]
        self.__matrixVect[:, 4] = imag[:]
        for i in range(1, len(self.__matrixVect)):
            previous = i - 1
            self.__matrixVect[i, 3:] = self.__matrixVect[i, 3:] + self.__matrixVect[previous, 3:]
        return self.__matrixVect[:, 2:]
