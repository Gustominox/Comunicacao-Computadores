import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('10.0.0.10', 3333))

msg = "Adoro Redes :)"

while True:
    s.sendall(msg.encode('utf-8'))
    time.sleep(1)
    
s.close()