#############################
# Author(s): Josh Cullings  #
#            James Eaton    #
#                           #
# Date: 9/23/2019           #
#########/###################

import socket as sc
import sys
import time

def player(host, port, x, y): # i.e. the client
    socket = sc.socket()
    socket.connect((host, port))

    socket.send(('200 x='+str(x)+'&y='+str(y)).encode())

    result = socket.recv(1024).decode()
    print(result)
    
    with open("opponent_board.txt") as f:
        opponent_board = f.read().splitlines()
        
    file = []
    newFile = []
    for i in range(0,10):
        for j in range (0,10):
            newFile.append(opponent_board[i][j])

        file.append(newFile)
        newFile = []

    if(result != '400'):
        x = int(x)
        y = int(y)
        opponent_board = file
        
        opponent_out = open("opponent_board.txt", 'w')

        if(len(result) > 5):
            if(result[8] == '1'):
                opponent_board[x][y] = 'X'

            elif(result[8] == '0'):
                opponent_board[x][y] = 'O'

        for i in range(0,10):
            opponent_out.write(''.join(opponent_board[i]))
            opponent_out.write("\n")

        socket.close()
        
    print('\n  0 1 2 3 4 5 6 7 8 9')
    for i in range(0,10):
        print(str(i)+' '+str(' '.join(opponent_board[i])))

if __name__ == '__main__':
    try:
        host = str(sys.argv[1])
        port = int(sys.argv[2])
        x = sys.argv[3]
        y = sys.argv[4]
        
        player(host, port, x, y)
    except:
        print("Please enter the correct parameters")

#########################################################################################################
# References:                                                           `                               #
#   https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a   #
#                                                                                                       #
#########################################################################################################
