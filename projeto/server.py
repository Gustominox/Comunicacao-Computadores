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

        innit_log(self.conf.getLogFile())

        self.DB = Cache()

        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)  # '10.0.0.1'
        self.porta = 3333

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

    def getDBLine(self, connection, address):
        while True:
            msg = connection.recv(1024)

            if not msg:
                debug("Conexao Terminada")
                break
            line = msg.decode('utf-8')
            self.DB.append(line)
            debug(f"Recebi uma ligação do cliente {address}")
        event.set()
        connection.close()

    def receive_DB(self):
        s = socket.socket(socket.AF_INET,     # Familia de enderecos ipv4
                          socket.SOCK_STREAM)  # Connection-Oriented (TCP PROTOCOL)

        s.bind(('', self.porta))
        s.listen()

        print(f"Estou à escuta no {self.endereco}:{self.porta}")

        while True:
            connection, address = s.accept()

            threading.Thread(target=self.getDBLine, args=(
                connection, address)).start()
            if(event.wait()):
                break

        s.close()

    def send_tcp_test(self, endereco='127.0.0.1', porta=3333):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((endereco, porta))

        i = 0
        while True and i < 10:
            msg = f"Adoro Redes :) [{i}]"
            s.sendall(msg.encode('utf-8'))
            time.sleep(1)
            i += 1

        s.close()

    def send_DB(self, endereco='127.0.0.1', porta=3333):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.connect((endereco, porta))

            for line in self.DB:
                print(line)
                s.sendall(line.encode('utf-8'))
                time.sleep(0.01)

            s.close()

        except:
            debug("Impossivel Conectar")
     # deprecated
    # def startConnection(self,endereco='127.0.0.1', porta=3333):
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

        for char in text:
            if char == '\n':
                if not remove and string != "":
                    print(string)
                    subString = ""
                    values = []
                    for c in string:
                        if c == ' ' and subString != "":
                            values.append(subString)
                            subString = ""
                        else:
                            subString += c

                    current_time = datetime.now()
                    timeStamp = current_time - self.startTime
                    # self.DB.addEntry(("Name", "Type", "Value", "TTL",
                                    #   "1", "FILE", str(timeStamp.total_seconds())))

                    self.DB.addEntry((values[0], values[1], values[2], values[3], "1",
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
            soc.sendto(msg.encode('utf-8'), (endereco, 3333))
            debug("Mensagem enviada")

        except:
            exception("Impossivel enviar mensagem")


def main():

    server_type = sys.argv[1]

    server = Server(server_type, "./etc/gusto.conf")

    if server.server_type == "SP":
        print(server.startTime)
        time.sleep(1)
        server.readDataBase(server.conf.getDBFile())
        print(server.DB)

        # server.send_DB()
    elif server.server_type == "SS":

        server.startConnection()

        while True:
            server.receive_DB()
            debug(server.DB)
    elif server.server_type == "SR":
        server.run_udp()


if __name__ == "__main__":
    main()
