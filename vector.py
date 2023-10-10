import math


class Vector:
    def __init__(self, length, pos, angle):
        self.x, self.y = pos
        self.angle = angle
        self.length = length

        self.vector = self.find_vector()

    def find_vector(self):
        x = self.length * math.cos(self.angle)
        y = self.length * math.sin(self.angle)

        return [x, y]