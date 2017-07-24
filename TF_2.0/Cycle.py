import pygame
from general import *

class Cycle:
    def __init__(self, color=None, direct=None, pos=None, path=[], alive=False):
        self.color = color          # (r, g, b)
        self.position = pos        # [x, y]
        self.direction = direct     # [x, y]
        self.path = path
        self.alive = alive


    def to_dict(self):
        d = {"color":self.color,
             "position":self.position,
             "direction":self.direction,
             "path":self.path,
             "alive":self.alive
        }
        return d

    def start(self, pos, direction):
        self.direction = dir_dict[direction]
        self.path.append([direction, self.position])
        self.position = pos


    def save_move(self, move):
        if self.path[-1][0] != move:
            self.path.append([move, self.position])


    # Precisa dos condicionais para evitar voltar na posição oposta
    def change_direction(self, direction):
        if direction == "l":    # left
            if self.direction != [1, 0]:
                self.direction = dir_dict['l']

        elif direction == "r":  # right
            if self.direction != [-1, 0]:
                self.direction = dir_dict['r']

        elif direction == "u":  # up
            if self.direction != [0, 1]:
                self.direction = dir_dict['u']

        elif direction == "d":  # down
            if self.direction != [0, -1]:
                self.direction = dir_dict['d']

        else:
            print("ERRO: Direção inválida")
            exit(0)


    def update(self):
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]
