import sys
import socket, pickle
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

def listen_for_messages():
    while True:
        data = s.recv(4096)
        payload = pickle.loads(data)
        if hasattr(payload, "__len__"):
            print("\n📝 — Grp Online Members")
            for user in payload:
                print("\t🟢 " + str(user[1]))
        else:
            message = payload.message
            print("\n" + message)
t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while True:
    print(f"Type 'q' to quit or 'w' to see who is online or send a chat to the grp")
    to_send = input()
    if to_send.lower() == 'q':
        break
    if to_send.lower() == 'w':
        payload = config.Payload()
        payload.request = "who is online"
        data = pickle.dumps(payload)
        s.send(data)
        continue
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    message = f"{c_color}[{date_now}] {name}{config.sep}{to_send}{Fore.RESET}\n"
    payload = config.Payload()
    payload.message = message
    data = pickle.dumps(payload)
    s.send(data)

sys.exit(1)