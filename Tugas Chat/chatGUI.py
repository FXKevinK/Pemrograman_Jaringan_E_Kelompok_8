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
		self.login.configure(width = 330,
							height = 350,
							bg="#E7E9D5")

		# create a Label
		self.nama = Label(self.login,
					text = "Progjar E: Eric, Feinard, Kevin", bg="#E7E9D5",
					justify = CENTER,
					font = "Roboto 8")

		self.nama.place(relheight = 0.15,
					relx = 0.25,
					rely = 0.01)

		# create a Label
		self.pls = Label(self.login,
					text = "Please login to continue", bg="#E7E9D5",
					justify = CENTER,
					font = "Roboto 13 bold")
		
		self.pls.place(relheight = 0.15,
					relx = 0.2,
					rely = 0.11)
		# create a Label
		self.labelName = Label(self.login,
							text = "Name: ", bg="#E7E9D5",
							font = "Roboto 12")
		
		self.labelName.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.2)
		
		# create a entry box for
		# tyoing the message
		self.entryName = Entry(self.login, border=5,
							font = "Roboto 14")
		
		self.entryName.place(relwidth = 0.4,
							relheight = 0.12, #0.12
							relx = 0.35,
							rely = 0.25) #0.2
		# create a Label
		self.labelNamePassword = Label(self.login, bg="#E7E9D5",
							text = "Password: ",
							font = "Roboto 12")
		
		self.labelNamePassword.place(relheight = 0.2,
							relx = 0.1,
							rely = 0.4)
		
		# create a entry box for
		# tyoing the message
		self.entryPassword = Entry(self.login,  border=5,
							font = "Roboto 14", show="*")
		
		self.entryPassword.place(relwidth = 0.4,
							relheight = 0.12, #0.12
							relx = 0.35,
							rely = 0.45) #0.4
		
		# set the focus of the curser
		self.entryName.focus()
		
		# create a Continue Button
		# along with action

		pc_btn = PhotoImage(file = '../img/pc1.png')

		self.go = Button(self.login,
						image = pc_btn, borderwidth=0, bg="#E7E9D5",
						#text = "Personal Chat",
						#font = "Roboto 14 bold",
						command = lambda: self.goAhead(self.entryName.get(),self.entryPassword.get()))
		
		self.go.place(relx = 0.15, #0.4
					rely = 0.65) #0.65

		
		gc_btn = PhotoImage(file = '../img/gc1.png')

		self.go2 = Button(self.login,
						image = gc_btn, borderwidth=0, bg="#E7E9D5",
						#text = "Group Chat",
						#font = "Roboto 14 bold",
						command = lambda: self.goAhead2(self.entryName.get(),self.entryPassword.get()))
		
		self.go2.place(relx = 0.5, #0.4
					rely = 0.65)

		
		file_btn = PhotoImage(file = '../img/files1.png')

		self.go3 = Button(self.login,
						image = file_btn, borderwidth=0, bg="#E7E9D5",
						#text = "Files",
						#font = "Roboto 14 bold",
						command = lambda: self.goAhead3(self.entryName.get(),self.entryPassword.get()))
		
		self.go3.place(relx = 0.35, #0.1
					rely = 0.83)

		self.Window.mainloop()

	def goAhead(self, name, password):
		self.login.destroy()
		self.goLogin(name, password)
		self.layout(name)
		# print(name)
		# print(password)

		# # the thread to receive messages
		rcv = threading.Thread(target=self.inbox)
		# rcv2 = threading.Thread(target=self.group_inbox)
		rcv.start()
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
							text = "Welcome " + self.name + "!",
							font = "Roboto 13 bold",
							pady = 5)
		
		self.labelHead.place(relwidth = 1)
		self.line = Label(self.Window,
						width = 450,
						bg = "#4352E6") #ABB2B9
		
		self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
		self.textCons = Text(self.Window,
							width = 20,
							height = 2,
							bg = "#E7E9D5", #17202A
							fg = "#17202A", #EAECEE
							font = "Roboto 14",
							padx = 5,
							pady = 5)
		
		self.textCons.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
		
		self.labelBottom = Label(self.Window,
								bg = "#4352E6", #ABB2B9
								height = 80)
		
		self.labelBottom.place(relwidth = 1,
							rely = 0.825)
		
		#TO Label

		self.labeltoboxp = Label(self.labelBottom, #bg="E7E9D5",
							# image = toboks, borderwidth=0,
							text = "To: ",
							font = "Roboto 12"
							)
		
		self.labeltoboxp.place(relheight = 0.03,
							relx = 0.15,
							rely = 0.007)
		
		#TO xxx BOX
		self.entryTo = Entry(self.labelBottom, border=3,
							bg = "#E0F6FF",#2C3E50
							fg = "#17202A", #EAECEE
							font = "Roboto 13")
		
		# place the given widget
		# into the gui window
		self.entryTo.place(relwidth = 0.45, #0.34
							relheight = 0.03,
							rely = 0.007,#0.008
							relx = 0.3)
		
		self.entryTo.focus()

		
		self.entryMsg = Entry(self.labelBottom, border=3,
							bg = "#E0F6FF", #2C3E50
							fg = "#17202A", #EAECEE
							font = "Roboto 13")
		
		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth = 0.70, #0.64
							relheight = 0.03,
							rely = 0.04,
							relx = 0.051
							)
		
		# self.entryMsg.focus()

		
		
		# create a Send Button
		self.buttonMsg = Button(self.labelBottom,
								text = "Send",
								font = "Futura 15 bold",
								width = 20,
								bg = "#FBE207", #ABB2B9
								command = lambda : self.sendButton(self.entryTo.get(), self.entryMsg.get()))
		
		self.buttonMsg.place(relx = 0.84, #0.77
							rely = 0.008,
							relheight = 0.06,
							relwidth = 0.12)
		
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
							text = "Welcome " + self.name + "! (Group1)",
							font = "Roboto 13 bold",
							pady = 5)
		
		self.labelHead.place(relwidth = 1)
		self.line = Label(self.Window,
						width = 450,
						bg = "#4352E6") #ABB2B9
		
		self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
		self.textCons = Text(self.Window,
							width = 20,
							height = 2,
							bg = "#E7E9D5", #17202A
							fg = "#17202A", #EAECEE
							font = "Roboto 14",
							padx = 5,
							pady = 5)
		
		self.textCons.place(relheight = 0.745,
							relwidth = 1,
							rely = 0.08)
		
		self.labelBottom = Label(self.Window,
								bg = "#4352E6", #ABB2B9
								height = 80)
		
		self.labelBottom.place(relwidth = 1,
							rely = 0.825)

		#TO Label

		# toboks = PhotoImage(file = '../img/pc1.png')

		self.labeltoboxg = Label(self.labelBottom, #bg="E7E9D5",
							# image = toboks, borderwidth=0,
							text = "To: ",
							font = "Roboto 12"
							)
		
		self.labeltoboxg.place(relheight = 0.03,
							relx = 0.15,
							rely = 0.007)
		
		#TO xxx BOX
		self.entryTo = Entry(self.labelBottom, border=3,
							bg = "#E0F6FF",#2C3E50
							fg = "#17202A", #EAECEE
							font = "Roboto 13")
		
		# place the given widget
		# into the gui window
		self.entryTo.place(relwidth = 0.45, #0.34
							relheight = 0.03,
							rely = 0.007,#0.008
							relx = 0.3)
		
		self.entryTo.focus()

		
		self.entryMsg = Entry(self.labelBottom, border=3,
							bg = "#E0F6FF", #2C3E50
							fg = "#17202A", #EAECEE
							font = "Roboto 13")
		
		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth = 0.70, #0.64
							relheight = 0.03,
							rely = 0.04,
							relx = 0.051
							)
		
		# self.entryMsg.focus()

		
		
		# create a Send Button

		# sena_btn = PhotoImage(file = '../img/send.png')

		self.buttonMsg = Button(self.labelBottom, 
								# image = sena_btn, borderwidth=0,
								text = "Send",
								font = "Futura 15 bold",
								width = 20,
								bg = "#FBE207", #ABB2B9
								command = lambda : self.sendButton2(self.entryTo.get(), self.entryMsg.get()))
		
		self.buttonMsg.place(relx = 0.84, #0.77
							rely = 0.008,
							relheight = 0.06,
							relwidth = 0.12)
		
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
							bg = "#E7E9D5") #17202A
		self.labelHead = Label(self.Window,
							bg = "#17202A",
							fg = "#EAECEE",
							text = "Files Transfer of " + self.name,
							font = "Roboto 13 bold",
							pady = 5)
		
		self.labelHead.place(relwidth = 1)
		self.line = Label(self.Window,
						width = 450,
						bg = "#4352E6") #ABB2B9
		
		self.line.place(relwidth = 1,
						rely = 0.07,
						relheight = 0.012)
		
		
		
		self.labelBottom = Label(self.Window,
								bg = "#4352E6", #ABB2B9
								height = 80)
		
		self.labelBottom.place(relwidth = 1,
							rely = 0.825)
		
		self.labelDownload = Label(self.Window,
								bg = "#E7E9D5") #ABB2B9

		self.labelDownload.place(relx = 0.4,
							rely = 0.84)
		
		self.filefrom = ttk.Combobox(values=['messi','henderson','lineker'])
		self.filefrom.place (relx=0.2,
								rely=0.3,
								anchor='center')

		self.fileListing = ttk.Combobox()
		self.fileListing.place (relx=0.8,
								rely=0.3,
								anchor='center')
		
				# create a Refresh Button (Optional)

		# senr_btn = PhotoImage(file = '../img/send.png')

		self.buttonDownload = Button(
								# image = senr_btn, borderwidth=0,
								text = "Download",
								font = "Futura 10 bold",
								width = 20,
								bg = "#FBE207", #ABB2B9
								command = lambda : self.downloadButton(self.filefrom.get(),self.fileListing.get()))
		
		self.buttonDownload.place(relx = 0.4,
							rely = 0.5,
							relheight = 0.07,
							relwidth = 0.22)
		
		#TO label

		self.labeltoboxf = Label(self.labelBottom, #bg="E7E9D5",
							# image = toboks, borderwidth=0,
							text = "To: ",
							font = "Roboto 12"
							)
		
		self.labeltoboxf.place(relheight = 0.03,
							relx = 0.15,
							rely = 0.007)
		
		#TO xxx BOX
		self.entryTo = Entry(self.labelBottom, border=3,
							bg = "#E0F6FF", #2C3E50
							fg = "#17202A", #EAECEE
							font = "Roboto 13")
		
		# place the given widget
		# into the gui window
		self.entryTo.place(relwidth = 0.45, #0.34
							relheight = 0.03,
							rely = 0.007, #0.007
							relx = 0.3)
		
		self.entryTo.focus()

		
		self.entryMsg = Entry(self.labelBottom, border=3,
							bg = "#E0F6FF", #2C3E50
							fg = "#17202A", #EAECEE
							font = "Roboto 13")
		
		# place the given widget
		# into the gui window
		self.entryMsg.place(relwidth = 0.70, #0.64
							relheight = 0.03,
							rely = 0.04,
							relx = 0.051
							)
		
		# self.entryMsg.focus()

		
		
		# create a Send Button
		self.buttonMsg = Button(self.labelBottom,
								text = "Send",
								font = "Futura 15 bold",
								width = 20,
								bg = "#FBE207", #ABB2B9
								command = lambda : self.sendButton3(self.entryTo.get(), self.entryMsg.get()))
		
		self.buttonMsg.place(relx = 0.84, #0.77
							rely = 0.008,
							relheight = 0.06, #0.03
							relwidth = 0.12) #0.22
		# 	# create a Refresh Button (Optional)
		# self.buttonRefresh = Button(self.labelBottom,
		# 						text = "Refresh",
		# 						font = "Roboto 10 bold",
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

	# YANG BARU
	# def fileLayout(self, name):

	# 	self.name = name
	# 	# to show chat window
	# 	self.Window.deiconify()
	# 	self.Window.title("FILES")
	# 	self.Window.resizable(width=False,
	# 						  height=False)
	# 	self.Window.configure(width=470,
	# 						  height=550,
	# 						  bg="#17202A")
	# 	self.labelHead = Label(self.Window,
	# 						   bg="#17202A",
	# 						   fg="#EAECEE",
	# 						   text="Welcome " + self.name + "!",
	# 						   font="Robotica 13 bold",
	# 						   pady=5)

	# 	self.labelHead.place(relwidth=1)
	# 	self.line = Label(self.Window,
	# 					  width=450,
	# 					  bg="#4352E6") #ABB2B9

	# 	self.line.place(relwidth=1,
	# 					rely=0.07,
	# 					relheight=0.012)

	# 	self.textCons = Text(self.Window,
	# 						 width=20,
	# 						 height=2,
	# 						 bg="#E7E9D5", #17202A
	# 						 fg="#17202A", #EAECEE
	# 						 font="Roboto 14",
	# 						 padx=5,
	# 						 pady=5)

	# 	self.textCons.place(relheight=0.745,
	# 						relwidth=1,
	# 						rely=0.08)

	# 	self.labelBottom = Label(self.Window,
	# 							 bg="#4352E6", #ABB2B9
	# 							 height=80)

	# 	self.labelBottom.place(relwidth=1,
	# 						   rely=0.825)

	# 	self.nameList =  ttk.Combobox(self.Window,
	# 							height=5,
	# 							textvariable='n'
	# 							)
	# 	nameList = self.inboxfile()
	# 	for i in nameList['messages']:
	# 		self.fileList.insert(END,i)

	# 	self.fileList = ttk.Combobox(self.Window,
	# 							height=5,
	# 							textvariable='n'
	# 							)

	# 	for i in nameList['messages'][self.nameList.get()]:
	# 		self.fileList.insert(END,)



	# 	# self.entryMsg.focus()

	# 	# create a Send Button
	# 	self.buttonMsg = Button(self.labelBottom,
	# 							text="Send",
	# 							font="Futura 15 bold",
	# 							width=20,
	# 							bg="#FBE207", #ABB2B9
	# 							command=lambda: self.sendButton(self.entryTo.get(), self.entryMsg.get()))

	# 	self.buttonMsg.place(relx=0.84, #0.77
	# 						 rely=0.008,
	# 						 relheight=0.06,
	# 						 relwidth=0.12) #0.22

	# 	self.textCons.config(cursor="arrow")

	# 	self.textCons.config(state=DISABLED)

	# def inboxfile(self):
	# 	if (self.tokenid == ""):
	# 		return "Error, not authorized"
	# 	string = "file_check {} \r\n".format(self.tokenid)
	# 	result = self.sendstring(string)
	# 	if result['status'] == 'OK':
	# 		return "{}".format(json.dumps(result['messages']))
	# 	else:
	# 		return "Error, {}".format(result['message'])

	# def group_inbox(self, groupid="group1"):
	# 	if (self.tokenid == ""):
	# 		return "Error, not authorized"
	# 	string = "group_inbox {} {}\r\n".format(self.tokenid, groupid)
	# 	result = self.sendstring(string)
	# 	if result['status'] == 'OK':
	# 		return "{}".format(json.dumps(result['message']))
	# 	else:
	# 		return "Error, {}".format(result['message'])

# create a GUI class object
g = GUI()
