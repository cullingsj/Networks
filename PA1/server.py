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

def checkMove(column, row):
    # Needs to be filled out
    return False

'''def loadBoard(filename):
    with open(f'{filename}') as csvfileIn:
        file = csv.reader(csvfileIn)
        data = list(file)
        print(file)'''

def battlefield(port, filename): # i.e. the host server
    host = sc.gethostname() # retreives the name of the local machine
    port = port # set variable to desired port number

    socket = sc.socket()
    socket.bind((host,port)) # connect host ip and desired port number

    while True:    
        socket.listen(1) # waits for connection
        player, address = socket.accept()
        
        while True: 
    
            print("New Connection found, initializing game.")
    
            board = loadBoard('own_board.txt')
    
            cords = player.revc(1024).decode()
            print(cords)
    
            #parce cords,BAD REQUEST?
            try:
                x = int(cords[2])
                y = int(cords[5])
            except:
                #return bad request
                player.send(("HTTP Bad Request").encode())
                break
           
            #bounds?    
            if(0<=x<=9)and(0<=y<=9):
            else:
                #return out of bounds
                player.send(("HTTP Not Found").encode())
                break

            #already hit?    
            if(board[x][y]='X') or (board[x][y]='O'):
                #return out of bounds
                player.send(("HTTP Gone").encode())
                break
            else:   
                if(board[x][y]!='_'): #hit
                    
                #sunk
                    
                else: #miss
                    board[x][y] = 'O'
                    #return miss
                    player.send(("HTTP OK hit=0").encode())
                    break
                
            #close inner loop
            break

'''        player.send(('Would you like to play a game?').encode())
        instructions = player.recv(1024).decode()
        
        if not instructions:
            break
        
        print('From player: ' + instructions)
        if(instructions == 'Yes' or 'yes' or 'y' or 'Y'):
            reply = 'Then let us begin'
            
        else:
            reply = 'you send me something?'
        player.send(reply.encode())'''
        #close connection
        player.close()

#main
if __name__ == '__main__':
    try:

	for line in fileinput.input(sys.argv[2]):
		print(line)

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
