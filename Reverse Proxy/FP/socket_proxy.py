from socket import *
import socket
import threading
import time
import sys
import logging


def ThrowingServer(data):
	images = ("localhost", 8889)
	pdf = ("localhost", 8890)
	default_server = ("localhost", 8888)
	request = data.split("\r\n")

	request = request[0].split(" ")
	request = request[1].strip()
	request = request.split("/")

	if request[1] == "images":
		return  images

	elif request[1] == "pdf":
		return pdf
	else:
		return default_server

class ProcessTheClient(threading.Thread):
	def __init__(self, connection, address):
		self.connection = connection
		self.address = address
		threading.Thread.__init__(self)

	def run(self):
		rcv=""
		while True:
			try:
				data = self.connection.recv(8192)
				data = data.decode()
				self.destination_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				if data:
					server = ThrowingServer(data)
					self.destination_sock.connect(server)
					self.destination_sock.sendall(data.encode())
					while(True):
						data_balasan = self.destination_sock.recv(1024)
						if(data_balasan == '' or data_balasan[-4:] == "\r\n\r\n"):
							print('break')
							break
						self.connection.sendall(data_balasan)
				else:
					break
			except OSError as e:
				pass
		self.connection.close()



class Server(threading.Thread):
	def __init__(self):
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		threading.Thread.__init__(self)

	def run(self):
		self.my_socket.bind(('0.0.0.0', 18000))
		self.my_socket.listen(1)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning("connection from {}".format(self.client_address))

			clt = ProcessTheClient(self.connection, self.client_address)
			clt.start()
			self.the_clients.append(clt)



def main():
	svr = Server()
	svr.start()

if __name__=="__main__":
	main()

