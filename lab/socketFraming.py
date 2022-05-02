import os, re
import fileReader

def send(socket, input, output):
    content = fileReader.fileReader(input) #gets contents
    byte_array = str(output).encode() + ' '.encode() + str(len(content)).encode() + ':'.encode() + content.encode() #appends importatnt info
    sent = ""

    while len(byte_array) != 0: #sends the whoole thing
        i = socket.send(byte_array) #sends little by little
        sent += byte_array[:i].decode()
        byte_array = byte_array[i:]
    return sent

def receive(socket):
    my_buff = ""
    my_buff = socket.recv(1024).decode() #received and saved in buffer

    start = my_buff.index(':')
    info = re.split(" ", my_buff[:start])
    destination = info[0]
    length = int(info[1]) #set initial and get info like size and destination
    actual = my_buff[start+1:]
    mssg = ""
    while len(mssg) < length: #keep reading buffer
        if len(actual) == 0:
            actual = socket.recv(1024).decode()
        mssg += actual[0]
        actual = actual[1:]

    path = "./server/" + destination
    fd = os.open(path, os.O_CREAT | os.O_WRONLY) #write only overwrites or makes
    os.write(fd, mssg.encode())
    os.close(fd)
    os.write(1, "File {} created.\n".format(destination).encode()) #write message on "server" or dest file

    return mssg

