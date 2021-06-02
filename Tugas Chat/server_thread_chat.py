from socket import *
import socket
from _thread import *
import time
import sys
import json
import logging
from chat import Chat
from collections import defaultdict as df

BUFFER_SIZE = 1024
chatserver = Chat()


class Server:
	def __init__(self):
		self.rooms = df(list)
		self.the_clients = []
		self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	def make_connection(self):
		self.my_socket.bind(('0.0.0.0', 8889))
		self.my_socket.listen(100)
		while True:
			self.connection, self.client_address = self.my_socket.accept()
			logging.warning("connection from {}".format(self.client_address))
			start_new_thread(self.clients, (self.connection,))

		self.my_socket.close()

	def clients(self, connection):
		data_buffer = connection.recv(BUFFER_SIZE).decode()
		data_buffer.split(" ")
		user_id = data_buffer[0]
		room_id = data_buffer[1]

		if room_id not in self.rooms:
			connection.send(f"Welcome {user_id}").encode()
		else:
			connection.send(f"welcome {user_id}, group of {room_id}").encode()

		self.rooms['room_id'].append(connection)

		while True:
			# command = "FILE/MESSAGE room_id message/file_name (option)size_file
			try:
				command = connection.recv(BUFFER_SIZE).decode()
				command.split(" ")
				if command[0] == "FILE":
					file_name = "{}" . format(command[2])
					size_file = "{}" . format(command[3])

					self.file_transport(connection, room_id, user_id, file_name, size_file)
				elif command[0] == "MESSAGE":
					for i in command[2:-1]:
						message = "{} {}" . format(message, i)
					self.group_broadcast(connection, room_id, user_id, message)
				else:
					self.connection_close(connection,room_id)
			except Exception as e:
				print(repr(e))
				break

	def file_transport(self, connection, room_id, user_id, file_name, size_file):
		for client in self.rooms[room_id]:
			if client != connection:
				try:
					#send to client = "FILE room_id message/file_name (option)size_file
					client.send("FILE {} {} {}" . format(file_name, size_file, user_id)).encode()
					time.sleep(0.1)
				except:
					client.close()
					self.connection_close(connection, room_id)

		data_send = 0
		while data_send < size_file:
			data = connection.recv(BUFFER_SIZE)
			for client in self.rooms[room_id]:
				try:
					client.send(data)
				except Exception as f:
					print(repr(f))
					client.close()
					self.connection_close(connection,room_id)
			data_send += len(data)


	def group_broadcast(self,connection, room_id, user_id, message):
		data_message = user_id + message
		message = data_message
		for client in self.rooms[room_id]:
			if client != connection:
				try:
					client.send(message.encode())
				except Exception as e:
					print(repr(e))
					client.close()
					self.connection_close(connection, room_id)

	def connection_close(self, connection, room_id):
		if connection in self.rooms[room_id]:
			self.rooms[room_id].remove(connection)

def main():
	svr = Server()
	svr.make_connection()


if __name__ == "__main__":
	main()
