import logging as log
import socket


class Server:

    def __init__(self):

        log.basicConfig(level=log.DEBUG,
                        format='%(asctime)s %(levelname)8s \t%(message)s',
                        filename='/tmp/server.log',
                        filemode='w',
                        datefmt='%d-%m-%y %H:%M:%S')

        self.soc = socket.socket(socket.AF_INET,     # Familia de aderecos ipv4
                                 socket.SOCK_DGRAM)  # Connection less (UDP PROTOCOL)

        self.hostname = socket.gethostname()
        self.endereco = socket.gethostbyname(self.hostname)  # '10.0.0.1'
        self.porta = 3333

    def run(self):

        self.soc.bind(('', self.porta))

        log.debug(f"Estou à escuta no {self.endereco}:{self.porta}")

        while True:
            msg, add = self.soc.recvfrom(1024)
            log.debug(f"MESSAGE RECEIVED: \"{msg.decode('utf-8')}\"")
            log.debug(f"Recebi uma mensagem do cliente {add}")

        self.soc.close()


def main():
    server = Server()
    server.run()


if __name__ == "__main__":
    main()
