from bottle import run, get, post, view, redirect, request
import requests, bottle, json, threading, time, sys, socket, pygame
from Cycle import *
from general import *


pygame.display.init()
screen = pygame.display.set_mode((100, 100))





#my_ip = socket.gethostbyname(socket.gethostname())
my_ip = "172.20.84.110"

try:
    port_ = int(sys.argv[1])
except:
    print("Please inform a valid port.\n")
    exit(0)


try:
    peers = sys.argv[2:]
    print(peers)

    peers_dict = {}
    for i in peers:
        peers_dict[i] = False
    peers_dict["http://" + my_ip + ":" + str(port_)] = True
except:
    print("Please inform a valid list of peers.\n")
    exit(0)




################################## GLOBAIS ####################################
my_id = "http://" + my_ip + ":" + str(port_)

board_size = (128, 72)
cell_size = 6
players = {}
##############################################################################

#################################### INIT ####################################
players[my_id] = Cycle((0, 255, 255), dir_dict['r'], [10, 10])
###############################################################################



@get('/peers')
def index():
	return json.dumps(peers)

@get('/get_data')
def index():
	return json.dumps(list_to_dict(players))



''' ########################## Funções das Threads ##########################'''
# Pegar a lista de peers de outros servidores
def get_peers():
    while True:
        for peer in peers:
            try:
                new_peers = requests.get(peer + "/peers")
                new_peers = json.loads(new_peers.text)
                for np in new_peers:
                    if np not in peers and peer != "http://" + my_ip:
                        peers.append(np)
            except:
                pass
            time.sleep(0.1)


# Pegar os dados com outros dervidores
def get_data():
    while True:
        for peer in peers:
            #if peer != "http://" + my_ip:
            try:
                row_data = requests.get(peer + "/get_data")
                data = json.loads(row_data.text)
                peers_dict[peer] = True
                for d in data:
                    if d != my_id:
                        players[d] = dict_to_cycle(data[d])
            except:
                peers_dict[peer] = False
            time.sleep(0.5)


# Tratar eventos
def get_events():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

                # Player keys
                if event.key == pygame.K_DOWN:
                    players[my_id].path.append(["D", (0, 0)])

                if event.key == pygame.K_UP:
                    players[my_id].path.append(["U", (0, 0)])

                if event.key == pygame.K_LEFT:
                    players[my_id].path.append(["L", (0, 0)])

                if event.key == pygame.K_RIGHT:
                    players[my_id].path.append(["R", (0, 0)])


# Exibir localmente
def show_data():
    while True:
        print("motor_cycles - BEGIN")
        for i in players:
            print(players[i].position, players[i].direction)
        print("motor_cycles - END")

        time.sleep(1)
''' ####################################################################### '''



########################## Funções de escrita na rede #########################
def dict_to_cycle(d):
    return Cycle(d["color"], d["direction"], d["position"], d["path"], d["alive"])

def list_to_dict(l):
    nd = {}
    for i in l:
        nd[i] = l[i].to_dict()
    return nd
###############################################################################

################################### Threads ###################################
t_get_data      = threading.Thread(target = get_data)
t_get_events    = threading.Thread(target = get_events)
t_show_data     = threading.Thread(target = show_data)
t_get_peers     = threading.Thread(target = get_peers)

t_get_data.start()
t_get_events.start()
t_show_data.start()
t_get_peers.start()
###############################################################################


run(host = my_ip, port = port_, quiet = True)
