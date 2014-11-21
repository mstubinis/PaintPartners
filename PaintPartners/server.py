import socket,select,Queue,json,random,sys,ConfigParser,getpass,imp
from threading import Thread
from time import sleep
from urllib2 import urlopen

def parse_message(message,typeMessage=""):
    messageList = []
    count = 0
    part = ''
    for char in message:
        if count != 0:
            if count > len(typeMessage)-1:
                if char == "_" or char == "|":
                    messageList.append(part)
                    part = ''
                else:
                    part += char
                    if count == len(message) - 1:
                        messageList.append(part)
                        part = ''
        count += 1
    return messageList

def GetIp():
    try:
        return json.load(urlopen('http://httpbin.org/ip'))['origin']
    except:
        print("Could not obtain IP Address")

def removekey(dictionary, key):
    r = dict(dictionary)
    del r[key]
    return r

class ServerListenThread(Thread):
    def __init__(self,server):
        super(ServerListenThread, self).__init__()
        self.running = True
        self.server = server

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = GetIp()
        self.port = 6121
        self.s.bind((self.host, self.port))
        print(str(self.host) + " Listening on port : " + str(self.port)+"\r\n")
        self.s.listen(10)
        
    def stop(self):
        self.running = False
    def run(self):
        while self.running:
            try:
                connection, address = self.s.accept()
                thread = ClientThread(self.server,connection,address[0])
                thread.start()
                self.server.clients[address[0]] = thread
            except socket.error as msg:
                print("Socket error!: " + str(msg))
                pass
                    
class ProcessThread(Thread):
    def __init__(self,server):
        super(ProcessThread, self).__init__()
        self.running = True
        self.q = Queue.Queue()
        self.server = server
        self.username = ""
    def add(self, data, username):
        self.q.put(data)
        self.username = username
    def stop(self):
        self.running = False
    def run(self):
        while self.running:
            if not self.q.empty():
                value = self.q.get(block=True)
                self.server.process(value,self.username)
                self.username = ""
                
            #clean up any innactive threads
            for key,value in self.server.clients.iteritems():
                if value.running == False:
                    print("Removing Client: " + str(key))
                    self.server.clients = removekey(self.server.clients,key)

class ClientThread(Thread):
    def __init__(self,server,socket,address):
        super(ClientThread, self).__init__()
        self.running = True
        self.conn = socket
        self.username = address
        self.address = address
        self.server = server
    def stop(self):
        self.running = False
    def run(self):
        while self.running:
            try:
                data = self.conn.recv(9999999)
                if data:
                    if not "_CONNECT_" in data:
                        self.server.process_thread.add(data,self.username)
                    else:
                        self.server.process_init(data,self)
            except socket.error as msg:
                print("Socket error!: " + str(msg))
                self.running = False
                pass
        print("Closing connection...")
        self.conn.close()

class InputThread(Thread):
    def __init__(self,server):
        super(InputThread, self).__init__()
        self.running = True
        self.server = server
    def run(self):
        while self.running:
            userinput = raw_input()
            if userinput == "print clients":
                self.server.print_clients()
            elif userinput == "print clients detail":
                self.server.print_clients_detail()
            elif userinput[:4] == "kick":
                if self.server.program.admin == userinput[5:]:
                    print("Cannot kick the admin from the server!")
                else:
                    self.server.reply_to_client_username("_KICK_",userinput[5:])
            elif userinput[:4] == "lock":
                self.server.reply_to_client_username("_LOCK_",userinput[5:])
            elif userinput[:6] == "unlock":
                self.server.reply_to_client_username("_UNLOCK_",userinput[7:])

class Server():
    def __init__(self):
        self.clients = {}
        self.admin = ""
        self.load_cfg()
    
        self.process_thread = ProcessThread(self)
        self.input_thread = InputThread(self)
        self.process_thread.start()
        self.input_thread.start()
        
        self.server_listen_thread = ServerListenThread(self)
        self.server_listen_thread.start()

        try:
            m = imp.load_source('main', 'main.pyw')
            self.program = m.Program(True)
        except:
            m = imp.load_source('main', 'main.py')
            self.program = m.Program(True)
            
    def print_clients(self):
        message = "\nConnected Clients: ["
        for key,value in self.clients.iteritems():
            message += str(key)+","
        message = message[:-1]
        message += "]\n"
        print(message)
        
    def print_clients_detail(self):
        print("\r\n----------------------------------")
        print("----------------------------------")
        print("Connected Clients")
        print("----------------------------------")
        for key,value in self.clients.iteritems():
            print("----------------------------------")
            print("Username:   " + str(value.username))
            print("Connected:  " + str(value.running))
            print("Address:    " + str(value.address))
            print("----------------------------------")
        print("----------------------------------\r\n")
        
        
    def load_cfg_yesorno(self,config,key,printstatement):
        while True:
            inputstr = raw_input(printstatement)
            if inputstr.lower() == "y":
                config.set('ServerInfo',key,"1")
                break
            elif inputstr.lower() == "n":
                config.set('ServerInfo',key,"0")
                break
            else:
                print("'"+inputstr+"' is not a valid answer.")
                
    def load_cfg(self):
        config = ConfigParser.RawConfigParser()
        try:
            config.readfp(open('server.cfg'))
        except Exception as e:
            config.add_section('ServerInfo')
            print('We need a moment to set up your server, please fill in the prompts below...')

            serverpassword = getpass.getpass("Please specify your server password: ")
            config.set('ServerInfo','serverpass',serverpassword)
            
            username = raw_input("Please specify your admin username: ")
            config.set('ServerInfo','adminname',username)
            
            self.load_cfg_yesorno(config,"AllowEdits","Allow clients to edit drawing board? (type 'y' for 'yes', 'n' for 'no'): ")
            #self.load_cfg_yesorno(config,"ClientDatabase","Restrict clients to specific names and passwords? (type 'y' for 'yes', 'n' for 'no'): ")

            with open('server.cfg', 'w') as configfile:
                config.write(configfile)
          
    def broadcast(self,message):
        for key,value in self.clients.iteritems():
            value.conn.send(message)
    def broadcast_notsource(self,message,username):
        for key,value in self.clients.iteritems():
            if key != username:
                value.conn.send(message)
                
    def reply_to_client(self,message,source_socket):
        source_socket.send(message)
        
    def reply_to_client_username(self,message,username):
        for key,value in self.clients.iteritems():
            if key == username:
                self.clients[username].conn.send(message)
                return
        print("Could not find username: " + username)

    def process_init(self,data,client_thread):
        if data:
            print(data)
            if "_CONNECT_" in data:
                messages = parse_message(data,"_CONNECT_")

                for key,value in self.clients.iteritems():
                    if key == messages[1]:
                        self.reply_to_client("_INVALIDUSERNAME_",client_thread.conn)
                        #client_thread.stop()
                        return
                config = ConfigParser.RawConfigParser()
                config.readfp(open('server.cfg'))
                serverPass = config.get('ServerInfo', 'serverpass')

                if messages[2] != serverPass:
                    self.reply_to_client("_INVALIDPASSWORD_",client_thread.conn)
                    #client_thread.stop()
                    return

                address_copy = client_thread.address
                client_thread.username = messages[1]
                self.clients[messages[1]] = client_thread
                self.clients = removekey(self.clients,address_copy)
                self.print_clients()

                canEdit = config.get('ServerInfo', 'allowedits')
                if canEdit == "1":
                    self.reply_to_client("_CONNECTVALID_",client_thread.conn)
                else:
                    self.reply_to_client("_CONNECTVALIDNOEDIT_",client_thread.conn)

    #This method prcesses string data          
    def process(self,data,username):
        if data:
            client_thread = None
            #get client thread to work with
            for key,value in self.clients.iteritems():
                if key == username:
                    client_thread = value
                    break
  
            if data[0] == "_":
                if "_CHATMESSAGE" in data:
                    #data[14:] - this should be the string data after the _CHATMESSAGE tag
                    self.broadcast(data[14:])

                elif "_PIXELDATA_" in data:
                    self.broadcast_notsource(data,username)
                elif "_REQUESTIMAGE_" in data:
                    imgdata = self.program.image.tostring()
                    self.reply_to_client_username("_FULLDATA_" + imgdata,username)
                elif "_DISCONNECT_" in data:
                    li = parse_message(data,"_DISCONNECT_")
                    print("Removing Client: " + li[1])
                    self.clients = removekey(self.clients,li[1])
                    
        
    def main(self):
        while True:
            self.program.main()
            
        self.process_thread.stop()
        self.process_thread.join()
        self.input_thread.stop()
        self.input_thread.join()
        self.server_listen_thread.stop()
        self.server_listen_thread.join()

if __name__ == "__main__":
    server = Server()
    server.main()
