''' Socket programming in python'''

import socket
import sys


try:
    s = socket.socket(socket.AF_INET,       # Familia de aderecos ipv4
                      socket.SOCK_STREAM)   # Connection Oriented (TCP PROTOCOL)
    print('Socket Successful')
except socket.error as error:
    print(f'Socket Failed: {error}')

port = 80

try:
    name = 'www.google.com'
    host_ip = socket.gethostbyname(name)
except socket.gaierror: # means that there is a problem with DNS
    print('Error resolving the host')
    sys.exit()
    
s.connect((host_ip,port))
print(f'Socket has connected to \"{name}\" on port == {host_ip}')
    
# getting a websites ip
# ip = socket.gethostbyname('www.google.com')
# print(ip)
