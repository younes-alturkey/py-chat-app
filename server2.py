import sys
import socket, pickle
import config
from threading import Thread

c_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((config.WS_SERVER_HOST, config.SERVER_SIDE_PORT_2))
s.listen(5)
print(
    f"\n🤡 — Accepting msgs from Load Balancer as localhost:{config.SERVER_SIDE_PORT_2}...\n")


# receive messages from load balancer
def listen_to_client(cs):
    while True:
        try:
            data = cs.recv(4096)
            payload = pickle.loads(data)
            if(payload.request == "who is online"):
                users = []
                for c_socket in c_sockets:
                    users.append(c_socket.getpeername())
                payload = pickle.dumps(users)
                for c_socket in c_sockets:
                    c_socket.send(payload)
            else:
                payload.message = payload.message.replace(config.sep, ": ")
                payload = pickle.dumps(payload)
                print("✅ — Publishing packets to client sockets...")
                for c_socket in c_sockets:
                    c_socket.send(payload)
        except Exception as e:
            c_sockets.remove(cs)


while True:
    # block until a load balancer client connects to the server and then returns a new socket object, and the address
    c_socket, c_address = s.accept()
    print(f"\n✅ — {c_address} is now connected.\n")
    c_sockets.add(c_socket)
    t = Thread(target=listen_to_client, args=(c_socket,))
    t.daemon = True
    t.start()

for cs in c_sockets:
    cs.close()
s.close()
