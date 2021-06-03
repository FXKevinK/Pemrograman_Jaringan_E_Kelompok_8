import sys
import os
import json
import uuid
import logging
from queue import Queue


class Chat:
    def __init__(self):
        self.sessions = {}
        # {
        # 	"member":["username1,username2,username3"]
        # 	"message":[
        # 	{
        # 		"message":"",
        # 		"from":""
        # 	},
        # 	{
        # 		"message":"",
        # 		"from":""
        # 	}
        # 	]
        # }
        self.groups = {}
        self.users = {}
        self.users['messi'] = {'nama': 'Lionel Messi',
                               'negara': 'Argentina',
                               'password': 'surabaya',
                               'incoming': {},
                               'outgoing': {},
                               'files': {}}
        self.users['henderson'] = {'nama': 'Jordan Henderson', 'negara': 'Inggris', 'password': 'surabaya',
                                   'incoming': {}, 'outgoing': {}, 'files': {}}
        self.users['lineker'] = {'nama': 'Gary Lineker', 'negara': 'Inggris', 'password': 'surabaya', 'incoming': {},
                                 'outgoing': {}, 'files': {}}
        self.groups['group1'] = {'nama': 'Group 1', 'member': ['messi', 'henderson', 'lineker'] , 'message': {}}

    def proses(self, data):
        print(f'data = {data}')
        j = data.split(" ")
        try:
            command = j[0].strip()
            if (command == 'auth'):
                username = j[1].strip()
                password = j[2].strip()
                logging.warning("AUTH: auth {} {}".format(username, password))
                return self.autentikasi_user(username, password)
            elif (command == 'send'):
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                message = ""
                for w in j[3:]:
                    message = "{} {}".format(message, w)
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning(
                    "SEND: session {} send message from {} to {}".format(sessionid, usernamefrom, usernameto))
                return self.send_message(sessionid, usernamefrom, usernameto, message)

            elif (command == 'group_send'):
                sessionid = j[1].strip()
                groupto = j[2].strip()
                usernamefrom = self.sessions[sessionid]['username']
                message = ""
                for w in j[3:]:
                    message = "{} {}".format(message, w)
                logging.warning("SEND: Group {} send message from {} with message".format(groupto, usernamefrom, message))
                return self.send_group(sessionid, groupto, usernamefrom, message)

            elif (command == 'file_send'):
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                filepath = j[3].strip()
                for i in j[4:-1]:
                    file_data = "{}{}".format()
                usernamefrom = self.sessions[sessionid]['username']
                logging.warning(
                    "SEND: session {} send file {} from {} to {}".format(sessionid, filepath, usernamefrom, usernameto,
                                                                         file_data))
                return self.send_file(sessionid, usernamefrom, usernameto, filepath)

            elif (command == 'inbox'):
                sessionid = j[1].strip()
                username = self.sessions[sessionid]['username']
                logging.warning("INBOX: {}".format(sessionid))
                return self.get_inbox(username)

            elif (command == 'group_inbox'):
                sessionid = j[1].strip()
                groupid = j[2].strip()
                username = self.sessions[sessionid]['username']
                logging.warning("INBOX: Group {} retrieve from {}".format(sessionid, groupid, username))
                return self.get_inbox_group(groupid, username)

            elif (command == 'file_check'):
                sessionid = j[1].strip()
                username = self.sessions[sessionid]['username']
                logging.warning("INBOX: {}".format(sessionid))
                return self.get_inbox_file(sessionid, username)

            elif (command == 'file_download'):
                sessionid = j[1].strip()
                usernameto = j[2].strip()
                filename = j[3].strip()
                logging.warning("DOWNLOAD: session {} file {}".format(sessionid, filename))
                username = self.sessions[sessionid]['username']
                return self.download_file(sessionid, username, usernameto, filename)

            else:
                return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
        except KeyError:
            return {'status': 'ERROR', 'message': 'Informasi tidak ditemukan'}
        except IndexError:
            return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}

    def autentikasi_user(self, username, password):
        if (username not in self.users):
            return {'status': 'ERROR', 'message': 'User Tidak Ada'}
        if (self.users[username]['password'] != password):
            return {'status': 'ERROR', 'message': 'Password Salah'}
        tokenid = str(uuid.uuid4())
        self.sessions[tokenid] = {'username': username, 'userdetail': self.users[username]}
        return {'status': 'OK', 'tokenid': tokenid}

    def get_user(self, username):
        if (username not in self.users):
            return False
        return self.users[username]

    def get_group(self, group):
        if (group not in self.groups):
            return False
        return self.groups[group]

    def send_message(self, sessionid, username_from, username_dest, message):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_dest)

        if (s_fr == False or s_to == False):
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        message = {'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message}
        outqueue_sender = s_fr['outgoing']
        inqueue_receiver = s_to['incoming']
        try:
            outqueue_sender[username_from].put(message)
        except KeyError:
            outqueue_sender[username_from] = Queue()
            outqueue_sender[username_from].put(message)
        try:
            inqueue_receiver[username_from].put(message)
        except KeyError:
            inqueue_receiver[username_from] = Queue()
            inqueue_receiver[username_from].put(message)
        return {'status': 'OK', 'message': 'Message Sent'}

    def send_group(self, sessionid, groupid, usernamefrom, message):
        if sessionid not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Not Found'}

        s_fr = self.get_user(usernamefrom)
        s_gr = self.get_group(groupid)
        if s_fr == False:
            return {'status': 'ERROR', 'message': 'User Not Found'}
        elif s_gr == False:
            return {'status': 'ERROR', 'message': 'Group Not Found'}

        message_out = {'msg_from': s_fr['nama'],
                       'msg_to': s_gr['member'],
                       'msg': message}
        outqueue_sender = s_fr['outgoing']  # self.users['Messi']['outgoing']
        inqueue_receiver = self.groups[groupid]['message']
        try:
            outqueue_sender[usernamefrom].put(message_out)
        except KeyError:
            outqueue_sender[usernamefrom] = Queue()
            outqueue_sender[usernamefrom].put(message_out)

        message_in = {'msg_from': s_fr['nama'],
                      'msg': message}
        try:
            inqueue_receiver[usernamefrom].put(message_in)
        except KeyError:
            inqueue_receiver[usernamefrom] = Queue()
            inqueue_receiver[usernamefrom].put(message_in)

        return {'status': 'OK', 'message': 'Message Sent To Group'}

    def send_file(self, sessionid, username_from, username_to, filename, file_data):
        if sessionid not in self.sessions:
            return {'status': 'ERROR', 'message': 'Session Not Found'}

        s_fr = self.get_user(username_from)
        s_to = self.get_user(username_to)
        if s_to == False or s_fr == False:
            return {'status': 'ERROR', 'message': 'User Tidak Ditemukan'}

        try:
            s_to['files'][username_from][filename] = file_data
        except KeyError:
            s_to['files'][username_from] = {}
            s_to['files'][username_from][filename] = file_data
        try:
            s_fr['files'][username_to][filename] = file_data
        except KeyError:
            s_fr['files'][username_to] = {}
            s_fr['files'][username_to][filename] = file_data

        return {'status': 'OK', 'message': 'Message Sent'}

    def get_inbox(self, username):
        s_fr = self.get_user(username)
        incoming = s_fr['incoming']
        msgs = {}
        for users in incoming:
            msgs[users] = []
            while not incoming[users].empty():
                msgs[users].append(s_fr['incoming'][users].get_nowait())

        return {'status': 'OK', 'messages': msgs}

    def get_inbox_group(self, groupid, username):
        s_fr = self.get_user(username)
        s_gr = self.get_group(groupid)
        incoming = s_gr['message']
        msgs = {}
        for users in incoming:
            msgs[users] = []
            while not incoming[users].empty():
                msgs[users].append(s_gr['message'][users].get_nowait())

        return {'status': 'OK', 'message': msgs}

    def get_inbox_file(self, sessionid, username):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_usr = self.get_user(username)
        files = s_usr['files']
        msgs = {}
        for user in files:
            msgs[user] = []
            for file in files[user]:
                msgs[user].append(file)
        return {'status': 'OK', 'messages': msgs}

    def download_file(self, sessionid, username_from, username_to, filename):
        if (sessionid not in self.sessions):
            return {'status': 'ERROR', 'message': 'Session Tidak Ditemukan'}
        s_usr = self.get_user(username_from)
        if (username_to not in s_usr['files']):
            return {'status': 'ERROR', 'message': 'File Tidak Ditemukan'}
        if filename not in s_usr['files'][username_to]:
            return {'status': 'ERROR', 'message': 'File Tidak Ditemukan'}
        data = s_usr['files'][username_to][filename]
        return {'status': 'OK', 'messages': f'Downloaded {filename}', 'filename': f'{filename}', 'data': f'{data}'}


if __name__ == "__main__":
    j = Chat()
    sesi = j.proses("auth messi surabaya")
    # print(sesi)
    # sesi = j.autentikasi_user('messi','surabaya')
    # print sesi
    tokenid = sesi['tokenid']
    print('inbox messi')
    print(j.get_inbox('messi'))
    print('send to messi and henderson')
    print(j.proses("send {} henderson hello gimana kabarnya son ".format(tokenid)))
    print(j.proses("send {} henderson mau tanya dikit dong henderson ".format(tokenid)))
    print(j.proses("send {} messi hello gimana kabarnya mess ".format(tokenid)))
    print('sending to group')
    print(j.proses("group_send {} group1 messi hello gimana kabarnya mess ".format(tokenid)))
    print(j.proses("group_send {} group1 henderson baik kabarku mess ".format(tokenid)))

    # print j.send_message(tokenid,'messi','henderson','hello son')
    # print j.send_message(tokenid,'henderson','messi','hello si')
    # print j.send_message(tokenid,'lineker','messi','hello si dari lineker')


    print("isi mailbox dari messi ke group")
    print(j.get_inbox_group('group1','messi'))
    print("isi mailbox dari henderson")
    print(j.get_inbox('henderson'))
