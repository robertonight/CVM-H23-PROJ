# Nom du fichier: utils.py
#
# Ce fichier contient des classes utilitaires pour l'implémentation d'une pile (classe FStack) et d'une liste chainée
# (classe LinkedList).
#
# Auteurs: Patrice Gallant et Roberto Nightingale
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


# https://realpython.com/linked-lists-python
class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " -> ".join(nodes)


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None
