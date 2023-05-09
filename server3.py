import sqlite3
import socket, pickle
import config
from threading import Thread

c_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((config.WS_SERVER_HOST, config.SERVER_SIDE_PORT_3))
s.listen(5)
print(f"\n🎃 — Accepting msgs from Load Balancer as localhost:{config.SERVER_SIDE_PORT_3}...\n")

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
                msg = payload.message
                payload = pickle.dumps(payload)
                print("✅ — Publishing packets to client sockets...")
                for c_socket in c_sockets:
                    c_socket.send(payload)

                peer_name = cs.getpeername()
                print("💾 — Saving chat history...")
                conn = sqlite3.connect('app.db')
                conn.execute("insert into history (group_id, user_id, message) values (?, ?, ?)", (config.SERVER_SIDE_PORT_3, peer_name[1], msg))
                conn.commit()
                print ("✔️ — Records created successfully")
                conn.close()
                print ("✅ — Chat history saved successfully.")
        except Exception as e:
            c_sockets.remove(cs)


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