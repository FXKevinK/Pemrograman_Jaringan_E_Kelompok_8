# import all the required modules
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
import base64
import socket
import os
import json
from io import StringIO
import time

TARGET_IP = "127.0.0.1"
TARGET_PORT = 8889

last_msg = ''
last_sender = ''
# GUI class for the chat
class GUI:
	# constructor method
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_address = (TARGET_IP,TARGET_PORT)
		self.sock.connect(self.server_address)
		self.tokenid=""
		# chat window which is currently hidden
		self.Window = Tk()
		self.Window.withdraw()
		
		# login window
		self.login = Toplevel()
		# set the title
		self.login.title("Login")
		self.login.resizable(width = False,
							height = False)
		self.login.configure(width = 400,
							height = 300)
		# create a Label
		self.pls = Label(self.login,
					text = "Please login to continue",
					justify = CENTER,
					font = "Helvetica 14 bold")
		
		self.pls.place(relheight = 0.15,
					relx = 0.2,
					rely = 0.07)
		# create a Label
		self.labelName = Label(self.login,
							text = "Name: ",
							font = "Helvetica 12")
		
		self.labelName.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.2)
		
		# create a entry box for
		# tyoing the message
		self.entryName = Entry(self.login,
							font = "Helvetica 14")
		
		self.entryName.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.2)
		# create a Label
		self.labelNamePassword = Label(self.login,
							text = "Password: ",
							font = "Helvetica 12")
		
		self.labelNamePassword.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.4)
		
		# create a entry box for
		# tyoing the message
		self.entryPassword = Entry(self.login,
							font = "Helvetica 14")
		
		self.entryPassword.place(relwidth = 0.4,
							relheight = 0.12,
							relx = 0.35,
							rely = 0.4)
		
		# set the focus of the curser
		self.entryName.focus()
		
		# create a Continue Button
		# along with action
		self.go = Button(self.login,
						text = "Personal Chat",
						font = "Helvetica 14 bold",
						command = lambda: self.goAhead(self.entryName.get(),self.entryPassword.get()))
		
		self.go.place(relx = 0.4,
					rely = 0.65)

		self.go2 = Button(self.login,
						text = "Group Chat",
						font = "Helvetica 14 bold",
						command = lambda: self.goAhead2(self.entryName.get(),self.entryPassword.get()))
		
		self.go2.place(relx = 0.4,
					rely = 0.85)

		self.go3 = Button(self.login,
						text = "Files",
						font = "Helvetica 14 bold",
						command = lambda: self.goAhead3(self.entryName.get(),self.entryPassword.get()))
		
		self.go3.place(relx = 0.1,
					rely = 0.85)

		self.Window.mainloop()

	def goAhead(self, name, password):
		self.login.destroy()
		self.goLogin(name, password)
		self.layout(name)
		# print(name)
		# print(password)

		# # the thread to receive messages
		rcv = threading.Thread(target=self.inbox)
		rcv.start()
		# rcv2 = threading.Thread(target=self.group_inbox)
		# rcv2.start()
		# self.group_inbox()
	

	def goAhead2(self, name, password):
		self.login.destroy()
		self.goLogin(name, password)
		self.layout2(name)
		# print(name)
		# print(password)

		# # the thread to receive messages
		# rcv = threading.Thread(target=self.inbox)
		# rcv.start()
		rcv2 = threading.Thread(target=self.group_inbox)
		rcv2.start()
	
	def goAhead3(self, name, password):
		self.login.destroy()
		self.goLogin(name, password)
		self.layout3(name)
		rcv3 = threading.Thread(target=self.file_inbox)
		rcv3.start()


	def sendstring(self,string):
		try:
			self.sock.sendall(string.encode())
			receivemsg = ""
			while True:
				data = self.sock.recv(64)
				# print("diterima dari server",data)
				if (data):
					receivemsg = "{}{}" . format(receivemsg,data.decode())  #data harus didecode agar dapat di operasikan dalam bentuk string
					if receivemsg[-4:]=='\r\n\r\n':
						# print("end of string")
						return json.loads(receivemsg)
		except:
			self.sock.close()
			return { 'status' : 'ERROR', 'message' : 'Gagal'}

	def goLogin(self,username,password):
		string="auth {} {} \r\n" . format(username,password)
		result = self.sendstring(string)
		if result['status']=='OK':
			self.tokenid=result['tokenid']
			return "username {} logged in, token {} " .format(username,self.tokenid)
		else:
			return "Error, {}" . format(result['message'])
	
	def file_inbox(self):
		while True:
			time.sleep(0.2)
			if (self.tokenid == ""):
				return "Error, not authorized"
			string = "file_check {} \r\n".format(self.tokenid)
			result = self.sendstring(string)	
			print (result)
			print (result['messages'])
			if result['status'] == 'OK':
				if str(result['messages']) == '''{}''':
					print("Empty File Inbox")
				else:
					sender = str(self.filefrom.get())		
					try:
						senderExist =  result['messages'][sender]
						fileList = ['']
						print(fileList)
						for i in senderExist:
							fileList.append(i)
						self.fileListing['values'] = fileList

						
					except:
						self.fileListing['values'] = ['']
						print("No files from selected user")
	
	def group_inbox(self, groupid="group1"):
		while True:
			time.sleep(1)
			if (self.tokenid == ""):
				return "Error, not authorized"
			string = "group_inbox {} {}\r\n".format(self.tokenid, groupid)
			result = self.sendstring(string)
			# print (result)
			if result['status'] == 'OK':
				time.sleep(0.2)
				#insert messages to text box
				self.textCons.config(state = NORMAL)
				io = StringIO()
				msg = json.dump(result['message'],io)
				iomsg = str(io.getvalue())
				# print(iomsg)

				if (iomsg == '''[]'''):
					# print('msh kosong')
					continue
				
				io2 = StringIO()
				from_msg = json.dump(result['message'][0]['msg_from'],io2)
				from_iomsg = str(io2.getvalue())
				from_iomsg = from_iomsg[1:-1]
				print(from_iomsg)

				io3 = StringIO()
				body_msg = json.dump(result['message'][0]['msg'],io3)
				body_iomsg = str(io3.getvalue())
				body_iomsg = body_iomsg[2:-5]
				print(body_iomsg)

				final_msg = ''
				final_msg = from_iomsg + ': ' + body_iomsg + '\n\n'

				global last_msg
				global last_sender
				# If mesagae already printed
				if (last_msg == final_msg and last_sender == from_iomsg):
					continue
				else:
					
					self.textCons.insert(END, final_msg)
					self.textCons.config(state = DISABLED)
					self.textCons.see(END)

				last_msg = final_msg
				last_sender = from_iomsg

			# 	final_msg = from_iomsg + ': ' + user_iomsg + '\n\n'

			# 	print(final_msg)
			
			# 	# print ("This is result")
			# 	# print (result)
			# 	# print ("This is msg: ")
			# 	# print (messi_msg)
			# 	# print ("iomsg: ")
			# 	# print (messi_iomsg)
				
			# 	self.textCons.insert(END, final_msg)
			# 	self.textCons.config(state = DISABLED)
			# 	self.textCons.see(END)

			# else:
			# 	print("tidak oke")
			# 	# return "Error, {}".format(result['message'])

	def goSendMessage(self,usernameto="xxx",message="xxx"):
			if (self.tokenid==""):
				return "Error, not authorized"
			string="send {} {} {} \r\n" . format(self.tokenid,usernameto,message)
			print(string)
			result = self.sendstring(string)
			if result['status']=='OK':
				return "message sent to {}" . format(usernameto)
			else:
				return "Error, {}" . format(result['message'])

	def sendgroupmessage(self,groupto="xxx",message="xxx"):
		if(self.tokenid==""):
			return "Error, not authorized"
		string="group_send {} {} {} \r\n" . format(self.tokenid,groupto,message)
		print(string)
		print(string)
		result = self.sendstring(string)
		print("ini result: ")
		print (result)
		if result['status'] == 'OK':
			return "message sent to {}".format(groupto)
		else:
			return "Error, {}".format(result['message'])

	
	def inbox(self):
		while True:
			if (self.tokenid==""):
				return "Error, not authorized"
			string="inbox {} \r\n" . format(self.tokenid)
			result = self.sendstring(string)
			if result['status']=='OK':
				time.sleep(0.2)
				# insert messages to text box
				self.textCons.config(state = NORMAL)
				io = StringIO()
				msg = json.dump(result['messages'],io)
				iomsg = str(io.getvalue())
				
				if (iomsg == '''{"messi": [], "henderson": [], "lineker": []}'''):
					# print('msh kosong')
					continue
				
				io2 = StringIO()
				messi_msg = json.dump(result['messages']['messi'],io2)
				messi_iomsg = str(io2.getvalue())

				io5 = StringIO()
				henderson_msg = json.dump(result['messages']['henderson'],io5)
				henderson_iomsg = str(io5.getvalue())

				io6 = StringIO()
				lineker_msg = json.dump(result['messages']['lineker'],io6)
				lineker_iomsg = str(io6.getvalue())

				final_msg = ''
				user_name = ''

				if (messi_iomsg != '[]'):
					user_name = 'messi'
				if (henderson_iomsg != '[]'):
					user_name= 'henderson'
				if (lineker_iomsg != '[]'):
					user_name = 'lineker'
				
				print(user_name)
				#MSG
				io3 = StringIO()
				user_msg = json.dump(result['messages'][user_name][0]['msg'],io3)
				user_iomsg = str(io3.getvalue())
				user_iomsg = user_iomsg[2:-5]

				#From
				io4 = StringIO()
				from_msg = json.dump(result['messages'][user_name][0]['msg_from'],io4)
				from_iomsg = str(io4.getvalue())
				from_iomsg = from_iomsg[1:-1]

				final_msg = from_iomsg + ': ' + user_iomsg + '\n\n'

				print(final_msg)
			
				# print ("This is result")
				# print (result)
				# print ("This is msg: ")
				# print (messi_msg)
				# print ("iomsg: ")
				# print (messi_iomsg)
				
				self.textCons.insert(END, final_msg)
				self.textCons.config(state = DISABLED)
				self.textCons.see(END)
				
				# return "{}" . format(json.dumps(result['messages']))
			else:
				return "Error, {}" . format(result['message'])


	# The main layout of the chat
	def layout(self,name):
		
		self.name = name
		# to show chat window
		self.Window.deiconify()
		self.Window.title("CHATROOM")
		self.Window.resizable(width = False,
							height = False)
		self.Window.configure(width = 470,
							height = 550,
							bg = "#17202A")
		self.labelHead = Label(self.Window,
							bg = "#17202A",
							fg = "#EAECEE",
							text = "welcome " + self.name + "!",
							font = "Helvetica 13 bold",
							pady = 5)
		
		self.labelHead.place(relwidth = 1)
		self.line = Label(self.Window,
						width = 450,
						bg = "#ABB2B9")
		
		self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
		self.textCons = Text(self.Window,
							width = 20,
							height = 2,
							bg = "#17202A",
							fg = "#EAECEE",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)
		
		self.textCons.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
		
		self.labelBottom = Label(self.Window,
								bg = "#ABB2B9",
								height = 80)
		
		self.labelBottom.place(relwidth = 1,
							rely = 0.825)
		
		#TO xxx BOX
		self.entryTo = Entry(self.labelBottom,
							bg = "#2C3E50",
							fg = "#EAECEE",
							font = "Helvetica 13")
		
		# place the given widget
		# into the gui window
		self.entryTo.place(relwidth = 0.34,
							relheight = 0.03,
							rely = 0.008,
							relx = 0.3)
		
		self.entryTo.focus()

		
		self.entryMsg = Entry(self.labelBottom,
							bg = "#2C3E50",
							fg = "#EAECEE",
							font = "Helvetica 13")
		
		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth = 0.64,
							relheight = 0.03,
							rely = 0.04,
							relx = 0.011
							)
		
		# self.entryMsg.focus()

		
		
		# create a Send Button
		self.buttonMsg = Button(self.labelBottom,
								text = "Send",
								font = "Helvetica 10 bold",
								width = 20,
								bg = "#ABB2B9",
								command = lambda : self.sendButton(self.entryTo.get(), self.entryMsg.get()))
		
		self.buttonMsg.place(relx = 0.77,
							rely = 0.008,
							relheight = 0.06,
							relwidth = 0.22)
		
		self.textCons.config(cursor = "arrow")
		
		# create a scroll bar
		scrollbar = Scrollbar(self.textCons)
		
		# place the scroll bar
		# into the gui window
		scrollbar.place(relheight = 1,
						relx = 0.974)
		
		scrollbar.config(command = self.textCons.yview)
		
		self.textCons.config(state = DISABLED)




# The main layout of the chat
	def layout2(self,name):
		
		self.name = name
		# to show chat window
		self.Window.deiconify()
		self.Window.title("CHATROOM")
		self.Window.resizable(width = False,
							height = False)
		self.Window.configure(width = 470,
							height = 550,
							bg = "#17202A")
		self.labelHead = Label(self.Window,
							bg = "#17202A",
							fg = "#EAECEE",
							text = "welcome " + self.name + "! (Group1)",
							font = "Helvetica 13 bold",
							pady = 5)
		
		self.labelHead.place(relwidth = 1)
		self.line = Label(self.Window,
						width = 450,
						bg = "#ABB2B9")
		
		self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
		self.textCons = Text(self.Window,
							width = 20,
							height = 2,
							bg = "#17202A",
							fg = "#EAECEE",
							font = "Helvetica 14",
							padx = 5,
							pady = 5)
		
		self.textCons.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
		
		self.labelBottom = Label(self.Window,
								bg = "#ABB2B9",
								height = 80)
		
		self.labelBottom.place(relwidth = 1,
							rely = 0.825)
		
		#TO xxx BOX
		self.entryTo = Entry(self.labelBottom,
							bg = "#2C3E50",
							fg = "#EAECEE",
							font = "Helvetica 13")
		
		# place the given widget
		# into the gui window
		self.entryTo.place(relwidth = 0.34,
							relheight = 0.03,
							rely = 0.008,
							relx = 0.3)
		
		self.entryTo.focus()

		
		self.entryMsg = Entry(self.labelBottom,
							bg = "#2C3E50",
							fg = "#EAECEE",
							font = "Helvetica 13")
		
		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth = 0.64,
							relheight = 0.03,
							rely = 0.04,
							relx = 0.011
							)
		
		# self.entryMsg.focus()

		
		
		# create a Send Button
		self.buttonMsg = Button(self.labelBottom,
								text = "Send",
								font = "Helvetica 10 bold",
								width = 20,
								bg = "#ABB2B9",
								command = lambda : self.sendButton2(self.entryTo.get(), self.entryMsg.get()))
		
		self.buttonMsg.place(relx = 0.77,
							rely = 0.008,
							relheight = 0.06,
							relwidth = 0.22)
		
		self.textCons.config(cursor = "arrow")
		
		# create a scroll bar
		scrollbar = Scrollbar(self.textCons)
		
		# place the scroll bar
		# into the gui window
		scrollbar.place(relheight = 1,
						relx = 0.974)
		
		scrollbar.config(command = self.textCons.yview)
		
		self.textCons.config(state = DISABLED)
	
	# Files Layout
	def layout3(self,name):
		
		self.name = name
		# to show chat window
		self.Window.deiconify()
		self.Window.title("CHATROOM")
		self.Window.resizable(width = False,
							height = False)
		self.Window.configure(width = 470,
							height = 550,
							bg = "#17202A")
		self.labelHead = Label(self.Window,
							bg = "#17202A",
							fg = "#EAECEE",
							text = "Files Transfer of " + self.name,
							font = "Helvetica 13 bold",
							pady = 5)
		
		self.labelHead.place(relwidth = 1)
		self.line = Label(self.Window,
						width = 450,
						bg = "#ABB2B9")
		
		self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
		
		
		self.labelBottom = Label(self.Window,
								bg = "#ABB2B9",
								height = 80)
		
		self.labelBottom.place(relwidth = 1,
							rely = 0.825)
		
		self.labelDownload = Label(self.Window,
								bg = "#ABB2B9")

		self.labelDownload.place(relx = 0.4,
							rely = 0.54)
		
		self.filefrom = ttk.Combobox(values=['messi','henderson','lineker'])
		self.filefrom.place (relx=0.2,
								rely=0.3,
								anchor='center')

		self.fileListing = ttk.Combobox()
		self.fileListing.place (relx=0.8,
								rely=0.3,
								anchor='center')
		
				# create a Refresh Button (Optional)
		self.buttonDownload = Button(
								text = "Download",
								font = "Helvetica 10 bold",
								width = 20,
								bg = "#ABB2B9",
								command = lambda : self.downloadButton(self.filefrom.get(),self.fileListing.get()))
		
		self.buttonDownload.place(relx = 0.5,
							rely = 0.5,
							relheight = 0.03,
							relwidth = 0.22)
		
		#TO xxx BOX
		self.entryTo = Entry(self.labelBottom,
							bg = "#2C3E50",
							fg = "#EAECEE",
							font = "Helvetica 13")
		
		# place the given widget
		# into the gui window
		self.entryTo.place(relwidth = 0.34,
							relheight = 0.03,
							rely = 0.008,
							relx = 0.3)
		
		self.entryTo.focus()

		
		self.entryMsg = Entry(self.labelBottom,
							bg = "#2C3E50",
							fg = "#EAECEE",
							font = "Helvetica 13")
		
		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth = 0.64,
							relheight = 0.03,
							rely = 0.04,
							relx = 0.011
							)
		
		# self.entryMsg.focus()

		
		
		# create a Send Button
		self.buttonMsg = Button(self.labelBottom,
								text = "Send",
								font = "Helvetica 10 bold",
								width = 20,
								bg = "#ABB2B9",
								command = lambda : self.sendButton3(self.entryTo.get(), self.entryMsg.get()))
		
		self.buttonMsg.place(relx = 0.77,
							rely = 0.008,
							relheight = 0.03,
							relwidth = 0.22)
		# 	# create a Refresh Button (Optional)
		# self.buttonRefresh = Button(self.labelBottom,
		# 						text = "Refresh",
		# 						font = "Helvetica 10 bold",
		# 						width = 20,
		# 						bg = "#ABB2B9",
		# 						command = lambda : self.refreshButton())
		
		# self.buttonRefresh.place(relx = 0.77,
		# 					rely = 0.043,
		# 					relheight = 0.03,
		# 					relwidth = 0.22)
		
		
		# self.textCons.config(cursor = "arrow")
		
		# self.textCons.config(state = DISABLED)

	# function to basically start the thread for sending messages
	def sendButton(self, to, msg):
		# self.textCons.config(state = DISABLED)
		# self.entryMsg.delete(0, END)
		print(msg)
		print (to)
		# snd= threading.Thread(target = self.goSendMessage(usernameto=to,message=msg))
		# snd.start()

		#print what u sent
		sent_msg = "You to " + to + ': ' + msg + '\n\n'; 
		self.textCons.insert(END, sent_msg)
		self.textCons.config(state = DISABLED)
		self.textCons.see(END)

		#send to server stuff
		self.goSendMessage(usernameto=to,message=msg)
	
	def refreshButton(self):
		self.file_inbox()
	
	def downloadButton(self, to, msg):
		downloadStatus = self.downloadfile(to,msg)
		print (downloadStatus)
		downloadStatus = downloadStatus[1:-1]
		self.labelDownload['text'] = downloadStatus

	def downloadfile(self, username, filename):
		if (self.tokenid == ""):
			return "Error, not authorized"
		string = "file_download {} {} {} \r\n".format(self.tokenid, username, filename)
		result = self.sendstring(string)
		if result['status'] == 'OK':
			output_file = open(result['filename'], 'wb')
			output_file.write(base64.b64decode(result['data']))
			output_file.close()
			return "{}".format(json.dumps(result['messages']))
		else:
			return "Error, {}".format(result['message'])
	
		# function to basically start the thread for sending messages
	def sendButton2(self, to, msg):
		# self.textCons.config(state = DISABLED)
		# self.entryMsg.delete(0, END)
		print(msg)
		print (to)
		# snd= threading.Thread(target = self.goSendMessage(usernameto=to,message=msg))
		# snd.start()

		# #print what u sent
		# sent_msg = "You to " + to + ': ' + msg + '\n\n'; 
		# self.textCons.insert(END, sent_msg)
		# self.textCons.config(state = DISABLED)
		# self.textCons.see(END)

		#send to server stuff
		self.sendgroupmessage(to,msg)
	
	def sendButton3(self, to, msg):
		print(msg)
		print (to)

		#send to server stuff
		self.sendfile(to,msg)
	
	def sendfile(self, usernameto, filename):
		if (self.tokenid == ""):
			return "Error, not authorized"
		try:
			file = open(filename, "rb")
		except FileNotFoundError:
			return "Error, {} file not found".format(filename)
		buffer = file.read()
		buffer_string = base64.b64encode(buffer).decode('utf-8')
		message = "send_file {} {} {} {} \r\n".format(self.tokenid, usernameto, filename, buffer_string)
		result = self.sendstring(message)
		if result['status'] == 'OK':
			return "file {} sent to {}".format(filename, usernameto)
		else:
			return "Error, {}".format(result['message'])

		


	# function to receive messages
	def receive(self):
		while True:
			try:
				message = client.recv(1024).decode(FORMAT)
				
				# if the messages from the server is NAME send the client's name
				if message == 'NAME':
					client.send(self.name.encode(FORMAT))
				else:
					# insert messages to text box
					self.textCons.config(state = NORMAL)
					self.textCons.insert(END,
										message+"\n\n")
					
					self.textCons.config(state = DISABLED)
					self.textCons.see(END)
			except:
				# an error will be printed on the command line or console if there's an error
				print("An error occured!")
				client.close()
				break
		
	# function to send messages
	def sendMessage(self):
		self.textCons.config(state=DISABLED)
		while True:
			message = (f"{self.name}: {self.msg}")
			client.send(message.encode(FORMAT))	
			break	

# create a GUI class object
g = GUI()
