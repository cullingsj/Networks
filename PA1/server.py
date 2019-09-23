#############################
# Author(s): Josh Cullings  #
#            James Eaton    #
#                           #
# Date: 9/23/2019           #
#########/###################

import socket as sc
import sys
import csv

def checkMove(column, row):
    # Needs to be filled out
    return False

def loadBoard(filename):
    with open(f'{filename}') as csvfileIn:
        file = csv.reader(csvfileIn)
        data = list(file)
        print(file)

def battlefield(port, filename): # i.e. the host server
    host = sc.gethostname() # retreives the name of the local machine
    port = port # set variable to desired port number

    socket = sc.socket()
    socket.bind((host,port)) # connect host ip and desired port number

    socket.listen(1) # waits for connection
    player, address = socket.accept()

    print("New Connection found, initializing game.")

    board = loadBoard('own_board.txt')

    while True:
        player.send(('Would you like to play a game?').encode())
        instructions = player.recv(1024).decode()
        
        if not instructions:
            break
        
        print('From player: ' + instructions)
        if(instructions == 'Yes' or 'yes' or 'y' or 'Y'):
            reply = 'Then let us begin'
            
        else:
            reply = 'you send me something?'
        player.send(reply.encode())
        
    player.close()

if __name__ == '__main__':
    try:
        port = int(sys.argv[1])
        boardFile = sys.argv[2]
        battlefield(port, boardFile)
    except:
        print('Invalid input')
    
#########################################################################################################
# References:                                                           `                               #
#   https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a   #
#   https://stackoverflow.com/questions/21233340/sending-string-via-socket-python                       #
#########################################################################################################