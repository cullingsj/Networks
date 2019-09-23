#############################
# Author(s): Josh Cullings  #
#            James Eaton    #
#                           #
# Date: 9/23/2019           #
#########/###################

import socket as sc

def player(): # i.e. the client
    host = sc.gethostname()
    port = 8990

    socket = sc.socket()
    socket.connect((host, port))

    data = socket.recv(1024).decode()

    print(data)
    reply = input('-> ')

    socket.send(reply.encode())

    if(reply == 'y' or 'Y' or 'Yes' or 'yes'):
        while True:
            data = socket.recv(1024).decode()
            print(data)
            
            message = input('Please enter an instruction with Column(A-J),Row(1-10), Ex: A8\n-> ')
            socket.send(message.encode())
        
    socket.close()

if __name__ == '__main__':
    player()

#########################################################################################################
# References:                                                           `                               #
#   https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a   #
#                                                                                                       #
#########################################################################################################
