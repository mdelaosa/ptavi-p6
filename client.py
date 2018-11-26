#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente que abre un socket a un servidor."""

import socket
import sys

try:
    method = sys.argv[1]  # Método usado.
    user = sys.argv[2].split(':')[0]  # Receptor+IP.
    server = user.split('@')[-1]  # IP.
    port = int(sys.argv[2].split(':')[-1])  # Puerto de ejecución.


# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto.
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_socket.connect((server, port))
        code = (method + ' sip:' + user + ' SIP/2.0\r\n\r\n')
        print(code)
        my_socket.send(bytes(code, 'utf-8'))
        data = my_socket.recv(1024)
        if method == 'INVITE' and data.decode('utf-8').split()[-2] == '200':
            my_socket.send(bytes('ACK sip:' + user + ' SIP/2.0\r\n\r\n',
                                 'utf-8'))
            print(data.decode('utf-8'))
        if method == 'BYE':
            print('FINISHING CONNECTION.')

except ConnectionRefusedError:
    print('CONNECTION ERROR')

except (IndexError, ValueError):
    sys.exit('Try: NAME@IP:PORT')
