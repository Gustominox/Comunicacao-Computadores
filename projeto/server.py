from debug_module import *
from config import config
import logging as log
import socket
import threading
import time

LOGFILE = '/tmp/server.log'


class Server:

    def __init__(self):

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

   

    def config(self, filename):
        try:
            self.conf.read(filename)
            debug("Leu config com sucesso")
        except:
            exception("Erro ao ler config")


def main():
    server = Server()
    server.config("./etc/sp.conf")
    debug(server.conf.getlines())
    server.run_tcp()


if __name__ == "__main__":
    main()
