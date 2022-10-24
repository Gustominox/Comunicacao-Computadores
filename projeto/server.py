import socket 

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
hostname = socket.gethostname()
endereco = socket.gethostbyname(hostname)   #'10.0.0.1'
porta = 3333
s.bind(('', porta ))

print(f"Estou à escuta no {endereco}:{porta}")

while True:
    msg, add = s.recvfrom(1024)
    print(msg.decode('utf-8'))
    print(f"Recebi uma mensagem do cliente {add}")

s.close()