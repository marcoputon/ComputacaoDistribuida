from bottle import run, get, post, view, redirect, request
import requests, bottle, json, threading, time, sys

try:
    port_ = int(sys.argv[1])
except:
    print("Please inform a valid port.\n")
    exit(0)

history = []


@get('/')
@view('chat.html')
def chat():
    return {'messages': history}


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



run(host = 'localhost', port = port_)
