from bottle import run, get, post, view, redirect, request
import requests, bottle, json, threading, time, sys

try:
    port_ = int(sys.argv[1])
except:
    print("Please inform a valid port.\n")
    exit(0)

try:
    peers = sys.argv[2:]
    print(peers)
except:
    print("Please inform a valid list of peers.\n")
    exit(0)

history = []



@get('/')
@view('chat.html')
def chat():
    return {'messages': history}


@get('/peers')
def index():
	return json.dumps(peers)


@get('/history')
def index():
	return json.dumps(history)


@get('/send_message')
@view('send_message.html')
def send_message():
    return


@post('/write_message')
def add_message():
    name = request.forms.get('name')
    msg = request.forms.get('msg')
    history.append([name, msg])

    redirect('/')


def get_peers():
    while True:
        for peer in peers:
            try:
                new_peers = requests.get(peer + "/peers")
                new_peers = json.loads(new_peers.text)
                for np in new_peers:
                    if np not in peers:
                        peers.append(np)
            except:
                pass
            time.sleep(1)

def receive_msg():
    while True:
        for peer in peers:
            try:
                new_h = requests.get(peer + "/history")
                new_h = json.loads(new_h.text)
                print(new_h)
                for m in new_h:
                    if m not in history:
                        history.append(m)
            except:
                pass

            time.sleep(1)


t_peers =   threading.Thread(target = get_peers)
t_chat  =   threading.Thread(target = receive_msg)

t_peers.start()
t_chat.start()

run(host = 'localhost', port = port_)
