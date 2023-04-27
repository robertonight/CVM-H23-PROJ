from PySide6.QtCore import Qt, Signal, Slot, QTimer, QPointF

class FStack:
    def __init__(self):
        self.__objects: list = []

    def __len__(self):
        return len(self.__objects)

    def front(self):
        return self.__objects[-1]

    def pop(self):
        return self.__objects.pop(-1)

    def push(self, obj):
        self.__objects.append(obj)

    def is_empty(self):
        return len(self.__objects) == 0

    def clear(self):
        self.__objects = []

    @property
    def objects(self):
        return self.__objects

    @objects.setter
    def set_objects(self, objects: list):
        if not isinstance(objects, list):
            raise Exception("ex..Pas de type liste")
        else:
            self.__objects = objects
