#! /usr//bin/env python3
# udp demo client.  Modified from Kurose/Ross by Eric Freudenthal 2016

from socket import *
import os
import sys, re                          

# default params
serverAddr = ('localhost', 50000)       

def usage():
    print("usage: %s [--serverAddr host:port]"  % sys.argv[0])
    sys.exit(1)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw in ("--serverAddr", "-s"):
            addr, port = re.split(":", args[0]); del args[0]
            serverAddr = (addr, int(port)) # addr can be a string (yippie)
        else:
            print("unexpected parameter %s" % args[0])
            usage();
except:
    usage()


print("serverAddr = %s" % repr(serverAddr))

clientSocket = socket(AF_INET, SOCK_DGRAM)
print("Input file name. Format: foo.extension")
fileName = sys.stdin.readline()[:-1]     # delete final \n
filePath = './%s' % (fileName)
fileExists=os.path.isfile(filePath)


if (fileExists):
    # True, proceed with sending filename (and data in the future)
    print("file found, or something like that")
    clientSocket.sendto(fileName.encode(), serverAddr)
    fileAck, serverAddrPort = clientSocket.recvfrom(2048)
    print('fileAck from %s is "%s"' % (repr(serverAddrPort), fileAck.decode()))

else:
    print ("file not found, exiting program")
        
#Do a check here to see if that fileName is valid, if so proceed, if not repeat?
