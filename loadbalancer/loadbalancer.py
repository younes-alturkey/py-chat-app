import sys
import config
import socket
import select
import random


def rr(iter):
    return next(iter)


class LoadBalancer(object):
    flow_table = dict()
    sockets = list()
    onlineUsers = list()

    def __init__(self, ip, port, algo='random'):
        self.ip = ip
        self.port = port
        self.algo = algo
        self.cs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # create client to server socket endpoint
        self.cs_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # connect the sockets to an address
        self.cs_socket.bind((self.ip, self.port))
        print("\n✅ — Initialized Load Balancer successfully.\n")
        print('🖧  — Listening to clients as %s ...\n' %
              (self.cs_socket.getsockname(),))
        self.cs_socket.listen(10)
        self.sockets.append(self.cs_socket)

    def start(self):
        while True:
            read_list, write_list, exception_list = select.select(
                self.sockets, [], [])
            for sock in read_list:
                if sock == self.cs_socket:
                    # when a new connection is accepted by a server socket
                    self.on_accept()
                    break
                else:
                    try:
                        data = sock.recv(4096)
                        if data:
                            self.on_receive(sock, data)
                        else:
                            self.on_close(sock)
                            break
                    except:
                        self.on_close(sock)
                        break

    # create a new client socket and connects to one of the backend servers.
    def on_accept(self):
        # block until a client connects to the server and then returns a new client socket object, and the address of the client
        c_socket, c_address = self.cs_socket.accept()
        print('✅ — New client connected %s `%s.' %
              (c_address, self.cs_socket.getsockname()))

        # apply the chosen load balancing algorithm and return the address of the chosen one
        server_ip, server_port = self.select(config.SERVER_POOL, self.algo)

        # create server-to-server socket endpoint
        ss_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            ss_socket.connect((server_ip, server_port))
            print('⭐ — Initializing server socket: %s ...\n' %
                  (ss_socket.getsockname(),))
            print('✅ — Connected to server %s %s.' % (
                ss_socket.getsockname(), (socket.gethostbyname(server_ip), server_port)))
            self.onlineUsers.append(ss_socket.getsockname()[1])
            print('online users are: ', self.onlineUsers)
        except:
            print("💩 — Couldn't establish connection with server socket, err: %s" %
                  sys.exc_info()[0])
            print("💩 — Closing connection with client socket %s" % (c_address,))
            c_socket.close()
            return

        # update the list to include the new sockets that have been created
        self.sockets.append(c_socket)
        self.sockets.append(ss_socket)

        # map each client socket to its corresponding server-to-server socket and vice versa
        self.flow_table[c_socket] = ss_socket
        self.flow_table[ss_socket] = c_socket

    # send the data to the appropriate backend server using the flow_table.
    def on_receive(self, sock, data):
        remote_socket = self.flow_table[sock]
        remote_socket.send(data)
        print('✅ — Sending packets: %-20s ==> %-20s' %
              (remote_socket.getsockname(), remote_socket.getpeername()))

    # remove socket from the list
    def on_close(self, sock):
        print('💩 — Client %s has disconnected from Load Balancer.' %
              (sock.getpeername(),))

        ss_socket = self.flow_table[sock]

        self.sockets.remove(sock)
        self.sockets.remove(ss_socket)
        self.onlineUsers.remove(ss_socket.getsockname()[1])
        print('online users are: ', self.onlineUsers)

        sock.close()
        ss_socket.close()

        del self.flow_table[sock]
        del self.flow_table[ss_socket]

    # select the appropriate algorithm for server selection
    def select(self, server_list, algo):
        if algo == 'random':
            return random.choice(server_list)
        elif algo == 'round robin':
            return rr(config.ITERATION)
        else:
            raise Exception('💀 — Unknown algorithm %s' % algo)


if __name__ == '__main__':
    try:
        LoadBalancer(config.WS_SERVER_HOST,
                     config.LOAD_BALANCER_SERVER_PORT, 'round robin').start()
    except KeyboardInterrupt:
        sys.exit(1)
