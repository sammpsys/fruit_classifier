'''

 Script to control the Jetank over a UDP server based on written input
 
'''
from socket import *

serverName = 'XXX.XXX.XXX.XX' # Personal IP Address on the Jetank (change this to your own IP address on your Jetank)
serverPort = 12000

# create UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)

while True:
    # get input from keyboard
    message = input('Message:')

    # Send message
    clientSocket.sendto(message.encode(), (serverName, serverPort))

# close UDP socket
clientSocket.close()
