import logging as log
import socket
import sys

from debug_module import *
from pdu_module import Pdu

LOGFILE = '/tmp/client.log'

DEBUG_MODE = True

 
pduText ='''# Header
MESSAGE-ID = 3874,FLAGS = Q+R,RESPONSE-CODE = 0,N-VALUES = 0,N-AUTHORITIES = 0,N-EXTRA-VALUES = 0,;
# Data: Query Info
QUERY-INFO.NAME = example.com.,QUERY-INFO.TYPE = MX,;
# Data: List of Response, Authorities and Extra Values
RESPONSE-VALUES = (Null)
AUTHORITIES-VALUES = (Null)
EXTRA-VALUES = (Null)'''
class Client:

    def __init__(self):

        innit_log(LOGFILE)


    def sendPDU(self,pdu,endereco):
        soc = socket.socket(socket.AF_INET,       # Familia de enderecos ipv4
                            socket.SOCK_DGRAM)    # Connection less (UDP PROTOCOL)

        msg = str(pdu)

        try:
            soc.sendto(msg.encode('utf-8'), (endereco, 3333))
            debug("Mensagem enviada")

        except:
            exception("Impossivel enviar mensagem")


def main():

    endereco = sys.argv[1]

    client = Client()
    pdu = Pdu(pduText)
    client.sendPDU(pdu,endereco)


if __name__ == "__main__":
    main()
