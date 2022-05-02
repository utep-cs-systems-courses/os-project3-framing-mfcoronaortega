#! /usr/bin/env python3

# Echo server program

import socket, sys, re, os
# sys.path.append("../lib")       #had to move params, not working otherwise
import params
import socketFraming

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedServer"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #listener socket
s.bind((listenAddr, listenPort))
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

while 1:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it) uses listener socket
    print('Connected to:', str(addr))
    conn.send("HELLO".encode()) #hello server
    try:
       socketFraming.receive(conn) #calls receive with connected socket
       os.write(1, "File transfer Complete.".encode())
       break
    except:
        print('Transfer failed\n')
        sys.exit()
        break
s.close()
