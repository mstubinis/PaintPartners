import sys,socket,thread,select,pygame,json,Queue,ConfigParser
from urllib2 import urlopen
from time import sleep
from threading import Thread

def GetIp():
    return json.load(urlopen('http://httpbin.org/ip'))['origin']

class ClientThreadSend(Thread):
    def __init__(self,client,socket):
        super(ClientThreadSend, self).__init__()
        self.running = True
        self.conn = socket
        self.q = Queue.Queue()
        self.client = client
    def add(self,data):
        self.q.put(data)
    def stop(self):
        self.conn.close()
        self.running = False
    def run(self):
        while self.running == True:
            try:
                if not self.q.empty():
                    message = self.q.get(block=True, timeout=1.0)
                    self.conn.send(message)
            except socket.error as msg:
                print("Socket error!: " +  str(msg))
                self.client.disconnect_from_server()
        self.conn.close()
class ClientThreadRecieve(Thread):
    def __init__(self,client,socket):
        super(ClientThreadRecieve, self).__init__()
        self.running = True
        self.conn = socket
        self.client = client
    def stop(self):
        self.conn.close()
        self.running = False
    def run(self):
        while self.running == True:
            try:
                data = self.conn.recv(16384)
                if data:
                    print(data)
                    if "_CONNECTVALID_" in data:
                        self.client.approve_connection()
                    elif "_KICK_" in data:
                        self.client.disconnect_from_server()
                    elif "_LOCK_" in data:
                        self.client.program.state = "STATE_MAIN_NOEDIT"
                    elif "_UNLOCK_" in data:
                        self.client.program.state = "STATE_MAIN"

                
            except socket.error as msg:
                print("Socket error!: " + str(msg))
                self.client.disconnect_from_server()
        self.conn.close()
        
class Client(object):
    def __init__(self,program):
        self.ip = GetIp()
        self.client_send = None
        self.client_recv = None
        self.connected = False
        self.connection_destination = ""
        self.username = ""
        self.server_pass = ""
        self.program = program

    def approve_connection(self):
        self.connected = True
        self.program.state = "STATE_MAIN"
        
    def connect_to_server(self,username,server,server_pass,admin=False):
        if username == "":
            return False
        if server == "":
            return False
        try:
            if self.connected == False:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.connection_destination = server
                if server.lower() == "localhost" or admin == True:
                    self.connection_destination = GetIp()

                self.username = username
                self.server_pass = server_pass
                if admin == True:
                    config = ConfigParser.RawConfigParser()
                    config.readfp(open('server.cfg'))
                    self.server_pass = config.get('ServerInfo', 'serverpass')

                client_socket.connect((self.connection_destination, 6121))

                
                self.client_send = ClientThreadSend(self,client_socket)
                self.client_send.start()
                self.client_recv = ClientThreadRecieve(self,client_socket)
                self.client_recv.start()
                
                self.send_message("_CONNECT_|" + self.username + "|" + self.server_pass)
                sleep(0.5)

                return True
            else:
                return False
        except Exception as e:
            print("Error: " + str(e))
            return False

    def disconnect_from_server(self,message=""):
        self.client_send.stop()
        self.client_recv.stop()
        self.connected = False
        self.program.state = "STATE_PROMPT"

        if message != "":
            pass

    def send_message(self,message):
        if self.client_send != None:       
            self.client_send.add(message)
