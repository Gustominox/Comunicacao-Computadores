import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('127.0.0.1', 3333))



i = 0
while True and i < 10:
    msg = f"Adoro Redes :) [{i}]"
    s.sendall(msg.encode('utf-8'))
    time.sleep(1)
    i += 1
    
s.close()