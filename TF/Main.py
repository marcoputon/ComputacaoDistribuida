import pygame
from pygame import *
from Board import *
from Cell import *
from Cycle import *
from time import sleep

display.init()

#   global variables
window = display.Info()

arena_size = (192, 108)
cell_size = 6
WIN_WIDTH = arena_size[0] * cell_size
WIN_HEIGHT = arena_size[1] * cell_size
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

screen = display.set_mode(DISPLAY)
display.set_caption("Pytron")

player = Cycle((24,202,230), [0, 0])
arena = Board(arena_size, player, cell_size, (5,13,16))
players = {}


print("resolution:", DISPLAY)



def main():
    init()

    #   game loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                #   move o player se estiver vivo
                if arena.player.alive:
                    # Player keys
                    if event.key == pygame.K_DOWN:
                        arena.player.change_direction("d")
                        arena.player.save_move("d")

                    if event.key == pygame.K_UP:
                        arena.player.change_direction("u")
                        arena.player.save_move("u")

                    if event.key == pygame.K_LEFT:
                        arena.player.change_direction("l")
                        arena.player.save_move("l")

                    if event.key == pygame.K_RIGHT:
                        arena.player.change_direction("r")
                        arena.player.save_move("r")

        if not arena.player.alive:
            flag = True
            for i in players:
                if players[i] == True:
                    flag = False
                    break
            if flag:
                restart(arena)

        arena.update()

        arena.draw(screen)
        pygame.display.update()
        sleep(0.02)



def restart(arena):
    arena.restart()
    count_down(arena)



def count_down(arena):
    size = 150
    myfont = pygame.font.SysFont("monospace", size)
    for i in range(3, 0, -1):
        screen.fill(Color("#8888ff"))
        arena.draw_grid(screen)

        label = myfont.render(str(i), 1, (216,218,231))
        screen.blit(label, (((WIN_WIDTH) / 2) - (size / 4), (WIN_HEIGHT - size) / 2))
        pygame.display.update()

        sleep(1)



if __name__ == "__main__":
    main()
