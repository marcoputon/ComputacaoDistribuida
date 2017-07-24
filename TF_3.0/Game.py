from bottle import run, get, post, view, redirect, request
import requests, bottle, json, threading, time, sys, socket
import pygame
import time
from Cycle import *

dir_dict = {'l':[-1, 0], 'r':[1, 0], 'u':[0, -1], 'd':[0, 1]}



class Game:
    def __init__(self):
        self.board_size = (128, 72)
        self.cell_size = 6
        self.screen = None
        self.ip = "172.20.84.110"
        self.port = 8000
        self.id = self.ip + ":" + str(self.port)
        self.players = {}

        self.peers = []

        # Threads
        self.t_get_data      = threading.Thread(target = self.get_data)
        self.t_get_events    = threading.Thread(target = self.get_events)
        self.t_show_data     = threading.Thread(target = self.show_data)
        self.t_get_peers     = threading.Thread(target = self.get_peers)

        # Inicializa o jogo antes de começar
        self.boot_game()


    def boot_game(self):
        pygame.display.init()
        self.screen = pygame.display.set_mode((self.board_size[0] * self.cell_size, self.board_size[1] * self.cell_size))
        ''' Cores
        background: (40, 44, 52)

        motos:
            azul ciano: (0, 255, 255)
            amarelo:    (255, 194, 23)
            laranja:    (255, 60, 46)
            rosa:       (148, 4, 94)

        '''

        self.players[self.id] = Cycle((0, 255, 255), dir_dict['r'], [10, 10])

        self.start_threads()

        run(host = self.ip, port = self.port, quiet = True)

    def run(self):
        pass

    def start_threads(self):
        self.t_get_data.start()
        self.t_get_events.start()
        self.t_show_data.start()
        self.t_get_peers.start()

    # Pegar a lista de peers de outros servidores
    def get_peers(self):
        while True:
            for peer in self.peers:
                try:
                    new_peers = requests.get(peer + "/peers")
                    new_peers = json.loads(new_peers.text)
                    for np in new_peers:
                        if np not in peers and peer != "http://" + self.id:
                            self.peers.append(np)
                except:
                    pass
                time.sleep(0.1)

    # Pegar os dados com outros dervidores
    def get_data(self):
        while True:
            for peer in self.peers:
                try:
                    row_data = requests.get(peer + "/get_data")
                    data = json.loads(row_data.text)
                    for d in data:
                        if d != self.id:
                            self.players[d] = dict_to_cycle(data[d])
                except:
                    pass
                time.sleep(0.1)

    # Desenhar
    def show_data(self):
        while True:
            for i in self.players:
                print(self.players[i].path)
            time.sleep(0.1)

    # Tratar eventos
    def get_events(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return

                    # Player keys
                    if event.key == pygame.K_DOWN:
                        self.players[self.id].save_move('d')

                    if event.key == pygame.K_UP:
                        self.players[self.id].save_move('u')

                    if event.key == pygame.K_LEFT:
                        self.players[self.id].save_move('l')

                    if event.key == pygame.K_RIGHT:
                        self.players[self.id].save_move('r')



@get('/peers')
def index():
	return json.dumps(Game.peers)

@get('/get_data')
def index():
	return json.dumps(list_to_dict(Game.players))

game = Game()
