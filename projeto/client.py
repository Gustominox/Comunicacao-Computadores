import logging as log
import socket
import sys
from debug_module import *

LOGFILE = '/tmp/client.log'

DEBUG_MODE = True


class Client:

    def __init__(self):

        innit_log(LOGFILE)

        self.soc = socket.socket(socket.AF_INET,       # Familia de aderecos ipv4
                                 socket.SOCK_DGRAM)    # Connection less (UDP PROTOCOL)

    def send(self, msg, endereco):
        try:
            self.soc.sendto(msg.encode('utf-8'), (endereco, 3333))
            debug("Mensagem enviada")

        except:
            exception("Impossivel enviar mensagem")


def main():

    endereco = sys.argv[1]

    msg = "Adoro Redes XD"

    client = Client()
    # print(f'{msg}  {endereco}')
    client.send(msg, endereco)


if __name__ == "__main__":
    main()
