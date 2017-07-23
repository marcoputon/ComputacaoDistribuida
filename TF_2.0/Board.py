from pygame import *
from Cell import *
from Cycle import *

class Board:
    def __init__(self, size, player, cs, color):
        self.color = color
        self.player = player
        self.cell_size = cs
        self.width = size[0]
        self.height = size[1]
        self.matrix = self.get_matrix(self.width, self.height)

    def restart(self):
        self.player.init([10, 10], ('r', [1, 0]))
        self.player.alive = True
        self.matrix = self.get_matrix(self.width, self.height)


    def get_matrix(self, width, height):
        m = []
        for i in range(width):
            line = []
            for j in range(height):
                line.append(Cell((i * self.cell_size, j * self.cell_size), self.cell_size, self.color))
            m.append(line)
        return m

    def update(self):
        if self.player.alive:
            self.player.update()

            # Colisão com as paredes
            if self.player.position[0] >= self.width or self.player.position[0] < 0 or self.player.position[1] >= self.height or self.player.position[1] < 0:
                self.player.die()
            elif self.matrix[self.player.position[0]][self.player.position[1]].color != self.color:
                self.player.die()
                self.matrix[self.player.position[0]][self.player.position[1]].color = (0, 0, 0)
            else:
                self.matrix[self.player.position[0]][self.player.position[1]].color = self.player.color

    def draw(self, surface):
        pos = self.player.position
        if self.player.alive:
            self.matrix[pos[0]][pos[1]].draw(surface)

    def draw_grid(self, surface):
        for i in self.matrix:
            for j in i:
                j.draw(surface)
