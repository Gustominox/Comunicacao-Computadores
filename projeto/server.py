import logging as log
import socket
import sys
import threading
import time

from config import config
from debug_module import *

LOGFILE = '/tmp/server.log'


class Server:

    def __init__(self,server_type):

        self.server_type = server_type
        innit_log(LOGFILE)

        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)  # '10.0.0.1'
        self.porta = 3333

        self.conf = config()

    def run_udp(self):

        soc = socket.socket(socket.AF_INET,     # Familia de aderecos ipv4
                            socket.SOCK_DGRAM)  # Connection less (UDP PROTOCOL)

        soc.bind(('', self.porta))

        debug(f"Estou à escuta no {self.endereco}:{self.porta}")

        while True:
            msg, add = self.soc.recvfrom(1024)
            debug(f"MESSAGE RECEIVED: \"{msg.decode('utf-8')}\"")
            debug(f"Recebi uma mensagem do cliente {add}")

        self.soc.close()

    def processamento(self, connection, address):
        while True:
            msg = connection.recv(1024)

            if not msg:
                debug("Conexao Terminada")
                break

            debug(msg.decode('utf-8'))
            debug(f"Recebi uma ligação do cliente {address}")

        connection.close()

    def run_tcp(self):
        s = socket.socket(socket.AF_INET,     # Familia de aderecos ipv4
                          socket.SOCK_STREAM)  # Connection-Oriented (UCP PROTOCOL)

        s.bind(('', self.porta))
        s.listen()

        print(f"Estou à escuta no {self.endereco}:{self.porta}")

        while True:
            connection, address = s.accept()

            threading.Thread(target=self.processamento, args=(
                connection, address)).start()

        s.close()

    def send_tcp(self, endereco='127.0.0.1', porta=3333):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        s.connect((endereco, porta))

        i = 0
        while True and i < 10:
            msg = f"Adoro Redes :) [{i}]"
            s.sendall(msg.encode('utf-8'))
            time.sleep(1)
            i += 1

        s.close()

    def config(self, filename):
        try:
            self.conf.read(filename)
            debug("Leu config com sucesso")
        except:
            exception("Erro ao ler config")


def main():
    
    server_type = sys.argv[1]
    
    server = Server(server_type)
    server.config("./etc/sp.conf")
    debug(server.conf.getlines())
    server.run_tcp()


if __name__ == "__main__":
    main()
