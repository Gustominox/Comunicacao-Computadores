import logging as log
import socket
import sys


class cliente:

    endereco = sys.argv[1]

    log.basicConfig(level=log.DEBUG,
                    format='%(asctime)s:%(levelname)-8s: %(message)s',
                    filename='/tmp/cliente.log',
                    filemode='w',
                    datefmt='%d-%m-%y %H:%M:%S')

    s = socket.socket(socket.AF_INET,       # Familia de aderecos ipv4
                      socket.SOCK_DGRAM)    # Connection less (UDP PROTOCOL)

    # hostname = socket.gethostname()
    # endereco = socket.gethostbyname(hostname)   #'10.0.0.1'

    msg = "Adoro Redes XD"
    try:
        s.sendto(msg.encode('utf-8'), (endereco, 3333))
        log.debug("Mensagem enviada")
    except:
        log.exception("Impossivel enviar mensagem")
