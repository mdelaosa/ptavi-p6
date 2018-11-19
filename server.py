#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            if line.decode('utf-8').split(' ')[0] == 'INVITE':
                print("THE CLIENT SENT: " + line.decode('utf-8'))
                self.wfile.write(b"SIP/2.0 100 TRYING...\r\n\r\n" +
                                 b"SIP/2.0 100 RINGING...\r\n\r\n" +
                                 b"SIP/2.0 200 OK...\r\n\r\n")
            if line.decode('utf-8').split(' ')[0] == 'BYE':
                print('FINISHING CONNECTION WITH THE CLIENT')
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', 6001), EchoHandler)
    print("Lanzando servidor SIP de eco...")
    try:
        """Creamos el servidor"""
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
