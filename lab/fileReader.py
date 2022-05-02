import re, os, sys

ibuf = ""  # Input buffer
sbuf = ""  # String buffer
sbufLength = 0  # String buffer length
currChar = 0  # Index of current char in sbuf


def my_getChar(fd):
    global ibuf
    global sbuf
    global sbufLength
    global currChar

    if currChar == sbufLength:  # If we reached the end of sbuf, get a new line and reset values
        ibuf = os.read(fd, 100)
        sbuf = ibuf.decode()
        sbufLength = len(sbuf)
        currChar = 0
        if sbufLength == 0:  # If we reached the end of the input, return nothing
            return ''

    char = sbuf[currChar]
    currChar += 1
    return char

def readLine(fd):
    char = my_getChar(fd)
    line = ""

    while char != '\n':  # While char is not equal to new line, keep getting chars for line
        line += char
        char = my_getChar(fd)
        if char == '':  # If char is empty, then we reached EOF; retun
            return line
    line += '\n'  # If a new line was found, then return the line with a new line char
    return line

def fileReader(myfile):
    fd = os.open(myfile, os.O_RDONLY) #opens file for read only
    contents = ""
    line = readLine(fd)
    while line != "EOF": #While we don't reach EOF (end of file)
        contents += line
        line = readLine(fd)
    return contents

