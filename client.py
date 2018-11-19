#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

try:
    METHOD = sys.argv[1] # Método usado.
    USER = sys.argv[2].split(':')[0] # Receptor+IP.
    SERVER = USER.split('@')[-1] # IP.
    PORT = int(sys.argv[2].split(':')[-1]) # Puerto de ejecución.

except (IndexError, ValueError):
    sys.exit('Try: NAME@IP:PORT')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    if METHOD == 'INVITE':
        my_socket.send(bytes('INVITE sip:' + USER + ' SIP/2.0\r\n', 'utf-8') + b'\r\n')
    if METHOD == 'BYE':
        my_socket.send(bytes('BYE sip: ' + USER + ' SIP/2.0\r\n', 'utf-8') + b'\r\n')
    try:
        data = my_socket.recv(1024)
        print('RECEIVED -- ', data.decode('utf-8'))
        print("FINISHING...")
    except ConnectionRefusedError:
        print('CONNECTION ERROR')

print("Fin.")
