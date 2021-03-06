import pygame
from pygame import *
from Board import *
from Cell import *
from Cycle import *
import time

from bottle import run, get, post, view, redirect, request
import requests, bottle, json, threading, sys


display.init()

#   global variables
window = display.Info()

arena_size = (128, 72)
cell_size = 6
WIN_WIDTH = arena_size[0] * cell_size
WIN_HEIGHT = arena_size[1] * cell_size
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

screen = display.set_mode(DISPLAY)
display.set_caption("Pytron")

player = Cycle((24, 202, 230), [0, 0])
arena = Board(arena_size, player, cell_size, (5,13,16))

init_pos = [10, 10]
my_ip = "192.168.0.8"
my_port = "8000"
my_id = my_ip + ":" + my_port
players = {my_id:[init_pos, player.color, player.path, False]}

peers = ["http://192.168.0.2:8000"]


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

                    print("TA VIVOOOOO")
                    # Player keys
                    if event.key == pygame.K_DOWN:
                        arena.player.change_direction("d")
                        arena.player.save_move("d")
                        players[my_id][0] = [init_pos]
                        players[my_id][2] = player.path

                    if event.key == pygame.K_UP:
                        arena.player.change_direction("u")
                        arena.player.save_move("u")
                        players[my_id][0] = [init_pos]
                        players[my_id][2] = player.path

                    if event.key == pygame.K_LEFT:
                        arena.player.change_direction("l")
                        arena.player.save_move("l")
                        players[my_id][0] = [init_pos]
                        players[my_id][2] = player.path

                    if event.key == pygame.K_RIGHT:
                        arena.player.change_direction("r")
                        arena.player.save_move("r")
                        players[my_id][0] = [init_pos]
                        players[my_id][2] = player.path
                else:
                    players[my_id][3] = False


        flag = True
        for i in players:
            print(i,  "DESGRAÇAAAAA")
            if players[i][3] == True:
                print("TEM ALGUEM VIVO")
                print(i)
                print()
                flag = False
                break
        if flag:
            print("TA TUDO MORTO")
            restart(arena)


        arena.update()
        for i in players:
            print(i, players[i])
            print()
        arena.draw(screen)
        pygame.display.update()
        time.sleep(0.02)



def restart(arena):
    for i in players:
        players[i][2] = []
    arena.restart()
    players[my_id][3] = True
    player.alive = True
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

        time.sleep(1)





''' BOTTLE STUFF '''
@get('/get_moves')
def index():
	return json.dumps(players)


def receive_msg():
    while True:
        for peer in list(players.keys()) + peers:
            try:
                new_h = requests.get(peer + "/get_moves")
                new_h = json.loads(new_h.text)
                print(peer)
                for i in new_h:
                    players[i] = new_h[i]

            except:
                pass

            time.sleep(0.5)

def server():
    run(host = my_ip, port = my_port)

receive_t  =   threading.Thread(target = receive_msg)
#peers_t  =   threading.Thread(target = get_peers)
server_t   =   threading.Thread(target = server)
game_t   =   threading.Thread(target = main)

receive_t.start()
#peers_t.start()
server_t.start()
game_t.start()
