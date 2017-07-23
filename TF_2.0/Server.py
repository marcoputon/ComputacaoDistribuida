from bottle import run, get, post, view, redirect, request
import requests, bottle, json, threading, time, sys, socket, pygame

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
except:
    print("Please inform a valid list of peers.\n")
    exit(0)


data_set = []


@get('/peers')
def index():
	return json.dumps(peers)

@get('/get_data')
def index():
	return json.dumps(data_set)

# Pegar a lista de peers de outros servidores
def get_peers():
    while True:
        for peer in peers:
            try:
                new_peers = requests.get(peer + "/peers")
                new_peers = json.loads(new_peers.text)
                for np in new_peers:
                    if np not in peers and d != "http://" + my_ip:
                        peers.append(np)
            except:
                pass
            time.sleep(0.1)

# Pegar os dados com outros dervidores
def get_data():
    while True:
        for peer in peers:
            try:
                row_data = requests.get(peer + "/get_data")
                data = json.loads(row_data.text)
                for d in data:
                    print(d, "http://" + my_ip)
                    if d not in data_set:
                        data_set.append(d)
                peers_dict[peer] = True
            except:
                peers_dict[peer] = False
            time.sleep(0.5)

# Tratar eventos
def get_events():
    while True:
        data = input()
        data_set.append(data)

# Exibir localmente
def show_data():
    while True:
        for i in data_set:
            print(i)

        for i in peers_dict:
            print(i, peers_dict[i])

        time.sleep(1)


### Threads ###
t1_dados    = threading.Thread(target = get_data)
t2_eventos  = threading.Thread(target = get_events)
t3_local    = threading.Thread(target = show_data)
t4_peers    = threading.Thread(target = get_peers)

t1_dados.start()
t2_eventos.start()
t3_local.start()
t4_peers.start()
###############


run(host = my_ip, port = port_, quiet = True)
