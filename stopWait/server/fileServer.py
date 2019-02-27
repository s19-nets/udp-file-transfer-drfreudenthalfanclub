#! /usr/bin/env python3
# udp demo -- simple select-driven uppercase server

# Eric Freudenthal with mods by Adrian Veliz

import sys
from socket import *
from select import select

serverAddr = ("", 50000)   # any addr, port 50,000

def verifyFile(sock):
  "run this function when sock has rec'd a message"
  fileName, clientAddrPort = sock.recvfrom(2048)
  print("from %s: rec'd '%s'" % (repr(clientAddrPort), repr(fileName)))
  AckMsg = fileName.decode()+"ACK"
  
  sock.sendto(AckMsg.encode(), clientAddrPort)
  

supperServerSocket = socket(AF_INET, SOCK_DGRAM)
supperServerSocket.bind(serverAddr)
supperServerSocket.setblocking(False)

# map socket to function to call when socket is....
readSockFunc = {}               # ready for reading
writeSockFunc = {}              # ready for writing
errorSockFunc = {}              # broken

timeout = 3                     #Allocates 3 seconds before failing each connection

# function to call when upperServerSocket is ready for reading
readSockFunc[supperServerSocket] = verifyFile

print("ready to receive")
timeoutNum = 0
while 1:
  readRdySet, writeRdySet, errorRdySet = select(list(readSockFunc.keys()),
                                                list(writeSockFunc.keys()), 
                                                list(errorSockFunc.keys()),
                                                timeout)
  if not readRdySet and not writeRdySet and not errorRdySet:
    print("timeout: no events")
    timeoutNum+=1
  if timeoutNum == 5:
    print("Timeout limit reached, disconnecting")
    break
  for sock in readRdySet:
    timeoutNum = 0 
    readSockFunc[sock](sock)

