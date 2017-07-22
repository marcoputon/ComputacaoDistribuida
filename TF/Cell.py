from pygame import *

class Cell:
    def __init__(self, pos, size, color):
        self.position = pos
        self.size = size
        self.color = color

    def draw(self, surface):
        draw.rect(surface, self.color, (self.position[0], self.position[1], self.size, self.size), 0)
