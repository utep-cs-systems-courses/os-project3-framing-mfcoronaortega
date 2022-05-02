#! /usr/bin/env python3

# Echo client program
import os
import socket, sys, re, time
sys.path.append("../lib")       # for params
import params
import socketFraming

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break


if s is None:
    print('could not open socket')
    sys.exit(1)

#Insert framing code
#need to establish connection
#prompt for file
while 1:
    try:
        welcome = s.recv(1024) #welcome message
        if welcome.decode() == "HELLO":
            os.write(1, "Welcome received:".encode())
            os.write(1, welcome.decode())
        print('\nEnter file name for communication:')
        file = os.read(0, 1024).decode()
        print('\nEnter file name for destination:')
        new_file = os.read(0, 1024).decode()
        print('\nSending contents')
        # file = "my_input.txt"
        # new_file = "test.txt"
        socketFraming.send(s, file, new_file) #send file #calls send with connected sock and src and dest
        break
    except:
        print('Failed Communication')
        sys.exit(1)
s.close()
