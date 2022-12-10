import logging as log
import socket
import sys
import threading
import time

from pdu_module import Pdu
from cache_module import Cache
from config_module import Config
from debug_module import *
from datetime import datetime

event = threading.Event()


class Server:

    def __init__(self, server_type, conf_file):

        self.startTime = datetime.now()

        self.server_type = server_type

        self.conf = Config(conf_file)

        innit_log(self.conf.logFile)

        self.DB = Cache()

        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)  # '10.0.0.1'
        self.porta = 55555

    def run_udp(self):

        soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                            socket.SOCK_DGRAM)  # Connection less (UDP PROTOCOL)

        soc.bind(('', self.porta))

        debug(f"Estou à escuta no {self.endereco}:{self.porta}",
              f"{self.endereco}:{self.porta}", )

        while True:
            msg, add = soc.recvfrom(1024)
            debug(f"MESSAGE RECEIVED: \"{msg.decode('utf-8')}\"")
            debug(f"Recebi uma mensagem do cliente {add}")

        self.soc.close()

  

    def startTZ(self,endereco='127.0.0.1', porta=55555):
        soc = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                          socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)

        soc.connect((endereco, porta))

        try:

            soc.sendall("REQUEST FOR TZ".encode('utf-8'))

        except:
            debug("Impossivel Conectar")
        
        msg = soc.recv(1024)
        line = msg.decode('utf-8')

        size = int(line)
        
        if size > self.DB.cacheSize - self.DB.cacheOccupancy:
            debug("TZ IS TOO BIG")
            return
        else:
            
            soc.sendall("OK TO SEND".encode('utf-8'))

            while True:
                
                msg = soc.recv(1024)
                print(msg)
                
                if not msg or msg.decode('utf-8') == "END OF TRANSFER":
                    debug("Conexao Terminada")
                    break
                line = msg.decode('utf-8')
                tuplo = tuple(map(str, line.replace('\'', '').replace(
                    '(', '').replace(')', '').split(', ')))

                
                current_time = datetime.now()
                timeStamp = current_time - self.startTime
                
                self.DB.addEntry((tuplo[0], tuplo[1], tuplo[2], tuplo[3], tuplo[4],
                                "SP", str(timeStamp.total_seconds())))

                
                # if(event.wait()):
                #     break
            soc.close()
            
        print("CLOSING SOCKET")    


    def answerTZ(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.bind(('', self.porta))            
        s.listen()

        connection, address = s.accept()
        msg = connection.recv(1024)
        line = msg.decode('utf-8')
        ################################################################
        ### check if msg received is request for TZ
        if (line == "REQUEST FOR TZ"):
            
            ### sending TZ size
            connection.sendall(str(self.DB.cacheOccupancy).encode('utf-8'))
            
            ### wanting for OK TO SEND
            msg = connection.recv(1024)
            line = msg.decode('utf-8')
            
            if (line == "OK TO SEND"):
            
        
            
            
                try:
                    # s.connect((endereco, porta))

                    for line in self.DB.table:
                        if line[8] == "VALID":
                            tuplo = line[:-2]
                            
                            connection.sendall(str(tuplo).encode('utf-8'))
                            time.sleep(1)
                    connection.sendall('END OF TRANSFER'.encode('utf-8'))


                except:
                    debug("Impossivel Conectar")
                    
                
            else:
                debug("SS CANT RECEIVE TZ")
        else:
            debug("WRONG HANDSHAKE")
            
        msg = connection.recv(1024)
        line = msg.decode('utf-8')
        print(line)    
        s.close()

    def send_tcp_test(self, endereco='127.0.0.1', porta=55555):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((endereco, porta))

        i = 0
        while True and i < 10:
            msg = f"Adoro Redes :) [{i}]"
            s.sendall(msg.encode('utf-8'))
            time.sleep(1)
            i += 1

        s.close()

    
    def readDataBase(self, DBfile):

        lines = []

        uncutLines = []
        remove = False
        fich = open(DBfile, "r")
        text = fich.read()

        string = ""
        NAME_DEFAULT = None
        for char in text:
            if char == '\n':
                if not remove and string != "":

                    subString = ""
                    values = []
                    for c in string:
                        if c == ' ' and subString != "":
                            if NAME_DEFAULT != None and subString == "@":
                                values.append(NAME_DEFAULT)
                                subString = ""
                            else:
                                values.append(subString)
                                subString = ""
                        else:
                            subString += c

                    current_time = datetime.now()
                    timeStamp = current_time - self.startTime
                    # TTL DEFAULT
                    if values[0] == "TTL" and values[1] == "DEFAULT":
                        TTL_DEFAULT = values[2]
                    
                    # NAME DEFAULT
                    elif values[0] == "@" and values[1] == "DEFAULT":
                        NAME_DEFAULT = values[2]
                        
                    # add entry to DB
                    else:
                       
                        if values[3] == "TTL":
                            TTL = TTL_DEFAULT
                        else:
                            TTL = values[3]
                       
                        if values.__len__() == 5:
                            ORDER = values[4]
                        else:
                            ORDER = 0
                            
                       
                        self.DB.addEntry((values[0], values[1], values[2], TTL, ORDER,
                                          "FILE", str(timeStamp.total_seconds())))
                string = ""
                remove = False
                continue

            string += char
            if char == '#':
                remove = True

    def sendPDU(self, pdu, endereco):
        soc = socket.socket(socket.AF_INET,       # Familia de enderecos ipv4
                            socket.SOCK_DGRAM)    # Connection less (UDP PROTOCOL)
        msg = str(pdu)
        try:
            soc.sendto(msg.encode('utf-8'), (endereco, 55555))
            debug("Mensagem enviada")

        except:
            exception("Impossivel enviar mensagem")
    
    def runTZ(self):
        while True:
          self.answerTZ()
          print(self.DB)
    
    def start(self):
        self.readDataBase(self.conf.DBFile)
    
        threading.Thread(target=self.runTZ()).start()
        
            
            
        

def main():

    server_type = sys.argv[1]

    server = Server(server_type, "./etc/gusto.conf")

    if server.server_type == "SP":
        server.start()
        time.sleep(1)
        

        print(server.DB)

        
    elif server.server_type == "SS":

        # server.startConnection()

        # while True:
        # threading.Thread(target=server.startTZ()).start()
        server.startTZ()
        debug(server.DB)
    
    
    elif server.server_type == "SR":
        server.run_udp()


if __name__ == "__main__":
    main()
