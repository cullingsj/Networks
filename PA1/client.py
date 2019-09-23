#############################
# Author(s): Josh Cullings  #
#            James Eaton    #
#                           #
# Date: 9/23/2019           #
#########/###################

import socket as sc
import sys
#import csv
import fileinput


def player(host, port, x, y): # i.e. the client
    socket = sc.socket()
    socket.connect((host, port))
    while True:
        print(data)
        
        socket.send(message.encode())
        
    socket.close()

if __name__ == '__main__':
    try:
        host = str(sys.argv[1])
        port = int(sys.argv[2])
        x = int(sys.argv[3])
        y = int(sys.argv[4])
        
        player(host, port, x, y)
        
    except:
        print('Invalid input')

#########################################################################################################
# References:                                                           `                               #
#   https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a   #
#                                                                                                       #
#########################################################################################################
