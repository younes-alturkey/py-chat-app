import sys
import socket
import config
from threading import Thread

c_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((config.WS_SERVER_HOST, config.SERVER_SIDE_PORT_3))
s.listen(5)
print(f"\n🤖 — Accepting msgs from Load Balancer as localhost:{config.SERVER_SIDE_PORT_3}...\n")

def listen_to_client(cs):
    while True:
        try:
            msg = cs.recv(1024).decode()
        except Exception as e:
            c_sockets.remove(cs)
        else:
            msg = msg.replace(config.sep, ": ")
            print("✅ — Publishing packets to client sockets...")
        for c_socket in c_sockets:
            c_socket.send(msg.encode())


while True:
    c_socket, c_address = s.accept()
    print(f"\n✅ — {c_address} is now connected.\n")
    c_sockets.add(c_socket)
    t = Thread(target=listen_to_client, args=(c_socket,))
    t.daemon = True
    t.start()

for cs in c_sockets:
    cs.close()
s.close()