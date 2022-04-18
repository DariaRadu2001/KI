import numpy as np

class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_name(self):
        return self.name

    def __str__(self):
        return "("+str(self.x) + " " + str(self.y) + ")"

    def euklid(self, node2):
        p1 = np.array((self.get_x(), self.get_y()))
        p2 = np.array((node2.get_x(), node2.get_y()))

        return np.linalg.norm(p1 - p2)

