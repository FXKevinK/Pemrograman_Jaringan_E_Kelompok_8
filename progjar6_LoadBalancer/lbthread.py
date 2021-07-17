import socket
import time
import sys
import threading
import logging


class BackendList:
    def __init__(self):
        self.servers=[]
        self.servers.append(('127.0.0.1',9006))
        self.servers.append(('127.0.0.1',9007))
        self.servers.append(('127.0.0.1',9008))
        self.servers.append(('127.0.0.1',9009))
        # self.servers.append(('127.0.0.1',9010))
        self.current=0
    def getserver(self):
        s = self.servers[self.current]
        self.current=self.current+1
        if (self.current>=len(self.servers)):
            self.current=0
        return s


class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address, destserver):
        self.connection = connection
        self.address = address
        self.destserver = destserver
        threading.Thread.__init__(self)

    def run(self):
        rcv = ""
        while True:
            try:
                data = self.connection.recv(8192)
                data = data.decode()
                self.dest_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if data:
                    server = self.destserver
                    logging.warning("koneksi diteruskan ke {}".format(server))
                    self.dest_sock.connect(server)
                    self.dest_sock.sendall(data.encode())
                    recvdata = self.dest_sock.recv(8192)
                    self.connection.sendall(recvdata)
                    break
                else:
                    break
            except OSError as e:
                pass
        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.bservers = BackendList()
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 2500))
        self.my_socket.listen(5)
        while True:
            try:
                self.connection, self.client_address = self.my_socket.accept()
                logging.warning("connection from {}".format(self.client_address))
                # time.sleep(0.1)
                clt = ProcessTheClient(self.connection, self.client_address ,self.bservers.getserver())
                clt.start()
            except OSError as e:
                pass

def main():
   svr = Server()
   svr.start()

if __name__=="__main__":
    main()


