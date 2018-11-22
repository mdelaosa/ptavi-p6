#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


class SIPHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        self.wfile.write(b"Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            METHOD = line.decode('utf-8').split(' ')
            if METHOD == 'INVITE':
                print("THE CLIENT SENT: " + line.decode('utf-8'))
                self.wfile.write(b"SIP/2.0 100 TRYING...\r\n\r\n" +
                                 b"SIP/2.0 100 RINGING...\r\n\r\n" +
                                 b"SIP/2.0 200 OK...\r\n\r\n")
            if METHOD == 'ACK':
                aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + sys.argv[3]
                print('Vamos a ejecutar', aEjecutar)
                os.system(aEjecutar)
                self.wfile.write(b"cancion.mp3 enviada \r\n\r\n")
            if METHOD == 'BYE':
                print('FINISHING CONNECTION WITH THE CLIENT')
            #if self.error(line.decode('utf-8').split(' ')):
                #self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
            if METHOD != 'INVITE' or 'ACK' or 'BYE':
                self.wfile.write(b"SIP/2.0 405 METHOD NOT ALLOWED\r\n\r\n")
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break


if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[2])
    serv = socketserver.UDPServer(('', PORT), SIPHandler)
    print("Lanzando servidor SIP de eco...")
    try:
        """Creamos el servidor"""
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
