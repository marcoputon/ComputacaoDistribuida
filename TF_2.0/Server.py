from bottle import run, get, post, view, redirect, request
import requests, bottle, json, threading, time, sys, socket, pygame
from Cycle import *
from general import *

my_ip = socket.gethostbyname(socket.gethostname())

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

my_motor_cycle = Cycle() # Moto do server atual
motor_cycles = {"http://" + my_ip + ":" + str(port_):my_motor_cycle} # Inicia com a moto do server atual


@get('/peers')
def index():
	return json.dumps(peers)

@get('/get_data')
def index():
	return json.dumps(list_to_dict(motor_cycles))


''' Funções das Threads '''
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
                    motor_cycles[d] = dict_to_cycle(data[d])
            except:
                peers_dict[peer] = False
            time.sleep(0.5)


# Tratar eventos
def get_events():
    while True:
        data = input()
        motor_cycles.append(data)


# Exibir localmente
def show_data():
    while True:
        print("motor_cycles - BEGIN")
        for i in motor_cycles:
            print(i, motor_cycles[i])
        print("motor_cycles - END")

        '''
        print("peers_dict")
        for i in peers_dict:
            print(i, peers_dict[i])
        '''
        time.sleep(1)


def dict_to_cycle(d):
    return Cycle(d["color"], d["direction"], d["position"], d["path"], d["alive"])

def list_to_dict(l):
    nd = {}
    for i in l:
        nd[i] = l[i].to_dict()
    return nd


######## Threads ########
t1_dados    = threading.Thread(target = get_data)
t2_eventos  = threading.Thread(target = get_events)
t3_local    = threading.Thread(target = show_data)
t4_peers    = threading.Thread(target = get_peers)

t1_dados.start()
t2_eventos.start()
t3_local.start()
t4_peers.start()
########################


run(host = my_ip, port = port_, quiet = True)