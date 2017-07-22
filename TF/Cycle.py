from pygame import *

d = {'l':[-1, 0], 'r':[1, 0], 'u':[0, -1], 'd':[0, 1]}

class Cycle:
    def __init__(self, color, direct):
        self.position = None        # [x, y]
        self.color = color          # (r, g, b)
        self.direction = direct     # [x, y] --->
        self.alive = False
        self.path = []
        self.distance = 0

    def init(self, pos, direction):
        self.direction = direction[1]
        self.path.append([direction[0], 0])
        self.position = pos

    def save_move(self, move):
        if self.path[-1][0] != move and d[move] == self.direction:
            self.path.append([move, self.distance])
            self.distance = 0

    def die(self):
        self.alive = False
        self.path = []
        self.direction = [0, 0]
        self.distance = 0

    def change_direction(self, direction):
        if direction == "l":    # left
            if self.direction != [1, 0]:
                self.direction = d['l']

        elif direction == "r":  # right
            if self.direction != [-1, 0]:
                self.direction = d['r']

        elif direction == "u":  # up
            if self.direction != [0, 1]:
                self.direction = d['u']

        elif direction == "d":  # down
            if self.direction != [0, -1]:
                self.direction = d['d']

        else:
            print("ERRO: Direção inválida")
            exit(0)

    def update(self):
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]
        self.distance += 1

        print(self.path)
