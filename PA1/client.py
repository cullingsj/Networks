#############################
# Author(s): Josh Cullings  #
#            James Eaton    #
#                           #
# Date: 9/23/2019           #
#########/###################

import socket as sc
import sys


def player(host, port, x, y): # i.e. the client
    socket = sc.socket()
    socket.connect((host, port))

    socket.send(('200 x='+str(x)+'&y='+str(y)).encode())

    result = socket.recv(1024).decode()
    print(result)
    
    socket.close()

if __name__ == '__main__':
    host = str(sys.argv[1])
    port = int(sys.argv[2])
    x = int(sys.argv[3])
    y = int(sys.argv[4])
    
    player(host, port, x, y)

#########################################################################################################
# References:                                                           `                               #
#   https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a   #
#                                                                                                       #
#########################################################################################################
