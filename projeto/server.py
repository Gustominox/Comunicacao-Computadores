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
        self.porta = 5555

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

    def getDBLine(self, socket):
        while True:
            msg = socket.recv(1024)

            if not msg:
                debug("Conexao Terminada")
                break
            line = msg.decode('utf-8')
            tuplo = tuple(map(str, line.replace('\'', '').replace(
                '(', '').replace(')', '').split(', ')))

            self.DB.addEntry(tuplo)

        event.set()
        socket.close()

    def startTZ(self,endereco='127.0.0.1', porta=5555):
        s = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                          socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)

        s.connect((endereco, porta))


        ################################################################

        try:

            s.sendall("REQUEST FOR TZ".encode('utf-8'))


        except:
            debug("Impossivel Conectar")
        
        msg = s.recv(1024)
        line = msg.decode('utf-8')

        size = int(line)
        
        if size > self.DB.cacheSize - self.DB.cacheOccupancy:
            debug("TZ IS TOO BIG")
            return
        else:
            ################################################################

            # s.bind(('', self.porta))
            # s.listen()
            s.sendall("OK TO SEND".encode('utf-8'))


            while True:
                # connection, address = s.accept()
                
                self.getDBLine(s)
                # threading.Thread(target=self.getDBLine, args=(
                # connection, address)).start()
                if(event.wait()):
                    break

            s.close()

    def answerTZ(self, endereco='127.0.0.1', porta=5555):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.bind(('', self.porta))
        s.listen()

        

        ################################################################
        
        
        
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
                            time.sleep(0.01)


                except:
                    debug("Impossivel Conectar")
                    
                s.close()
            else:
                debug("SS CANT RECEIVE TZ")
        else:
            debug("WRONG HANDSHAKE")
            

    def send_tcp_test(self, endereco='127.0.0.1', porta=5555):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((endereco, porta))

        i = 0
        while True and i < 10:
            msg = f"Adoro Redes :) [{i}]"
            s.sendall(msg.encode('utf-8'))
            time.sleep(1)
            i += 1

        s.close()

     # deprecated
    # def startConnection(self,endereco='127.0.0.1', porta=5555):
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #     try :
    #         s.connect((endereco, porta))
    #         msg = ""
    #         s.sendall(line.encode('utf-8'))

    #         s.close()

    #     except: debug("Impossivel Conectar")

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
            soc.sendto(msg.encode('utf-8'), (endereco, 5555))
            debug("Mensagem enviada")

        except:
            exception("Impossivel enviar mensagem")


def main():

    server_type = sys.argv[1]

    server = Server(server_type, "./etc/gusto.conf")

    if server.server_type == "SP":
        time.sleep(1)
        server.readDataBase(server.conf.DBFile)

        print(server.DB)

        server.answerTZ()
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
