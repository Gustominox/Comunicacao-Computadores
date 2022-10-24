import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

hostname = socket.gethostname()
endereco = socket.gethostbyname(hostname)   #'10.0.0.1'


msg = "Adoro Redes :)"

s.sendto(msg.encode('utf-8'), ('10.2.2.1', 3333))
