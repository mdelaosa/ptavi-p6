#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

try:
    METHOD = sys.argv[1]  # Método usado.
    USER = sys.argv[2].split(':')[0]  # Receptor+IP.
    SERVER = USER.split('@')[-1]  # IP.
    PORT = int(sys.argv[2].split(':')[-1])  # Puerto de ejecución.

except (IndexError, ValueError):
    sys.exit('Try: NAME@IP:PORT')

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    if METHOD == 'INVITE' or METHOD == 'BYE':
        my_socket.send(bytes(METHOD + ' sip:' + USER + ' SIP/2.0\r\n',
                             'utf-8') + b'\r\n')
    try:
        data = my_socket.recv(1024)
        print('RECEIVED -- ', data.decode('utf-8'))
        print("FINISHING...")
        for message in data.decode('utf-8').split(" "):
            if message == '200 OK' and METHOD != 'BYE':
                my_socket.send(bytes('ACK sip:' + USER + ' SIP/2.0\r\n',
                                     'utf-8') + b'\r\n')
    except ConnectionRefusedError:
        print('CONNECTION ERROR')

print("Fin.")
