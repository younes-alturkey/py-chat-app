import sys
import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
import config

init()

c_color = random.choice(config.colors)


s = socket.socket()
print(f"\n⭐ — Connecting to Load Balancer {config.WS_SERVER_HOST}:{config.LOAD_BALANCER_SERVER_PORT}...\n")

s.connect((config.WS_SERVER_HOST, config.LOAD_BALANCER_SERVER_PORT))
print("✅ — Connected to Load Balancer.\n")

name = input("Type your name: ")
print("\n")

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    to_send = input()
    if to_send.lower() == 'q':
        break
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{c_color}[{date_now}] {name}{config.sep}{to_send}{Fore.RESET}\n"
    s.send(to_send.encode())

sys.exit(1)