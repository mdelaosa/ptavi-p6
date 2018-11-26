#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de SIP simple.
"""

import socketserver
import sys
import os


class SIPHandler(socketserver.DatagramRequestHandler):
    """
    SIP server class.
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address).
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente.
            line = self.rfile.read()
            if not line:
                break
            linea = line.decode('utf-8')
            (method, address, sip) = linea.split()
            print("THE CLIENT SENT: " + linea)
            if method == 'INVITE':
                self.wfile.write(b"SIP/2.0 100 TRYING...\r\n\r\n" +
                                 b"SIP/2.0 100 RINGING...\r\n\r\n" +
                                 b"SIP/2.0 200 OK...\r\n\r\n")
                break
            if method == 'ACK':
                song = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + sys.argv[3]
                print('SONG', song)
                os.system(song)
                self.wfile.write(b"cancion.mp3 SENT \r\n\r\n")
                print('hola')
                break
            if method == 'BYE':
                print('FINISHING CONNECTION WITH THE CLIENT')
                break
            if len(line.decode('utf-8').split(" ")) != 3:
                self.wfile.write(b"SIP/2.0 400 BAD REQUEST\r\n\r\n")
                break
            else:
                self.wfile.write(b"SIP/2.0 405 METHOD NOT ALLOWED\r\n\r\n")
                break


if __name__ == "__main__":
    # Creamos servidor y escuchamos.
    port = int(sys.argv[2])
    serv = socketserver.UDPServer(('', port), SIPHandler)
    print("STARTING SERVER...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("FINISHING SERVER")
