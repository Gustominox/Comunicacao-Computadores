import logging as log
import socket
import sys
from debug_module import *

LOGFILE = '/tmp/client.log'

DEBUG_MODE = True

 
pdu ='''
# Header
MESSAGE-ID = 3874, FLAGS = Q+R, RESPONSE-CODE = 0,
N-VALUES = 0, N-AUTHORITIES = 0, N-EXTRA-VALUES = 0,;
# Data: Query Info
QUERY-INFO.NAME = example.com., QUERY-INFO.TYPE = MX,;
# Data: List of Response, Authorities and Extra Values
RESPONSE-VALUES = (Null)
AUTHORITIES-VALUES = (Null)
EXTRA-VALUES = (Null) '''
class Client:

    def __init__(self):

        innit_log(LOGFILE)

        self.soc = socket.socket(socket.AF_INET,       # Familia de enderecos ipv4
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
    client.send(pdu, endereco)


if __name__ == "__main__":
    main()
