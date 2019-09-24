#############################
# Author(s): Josh Cullings  #
#            James Eaton    #
#                           #
# Date: 9/23/2019           #
#########/###################

import socket as sc
import sys
import csv
import fileinput

def writeOut(outFile, board):
    for i in range(0,10):
        for j in range(0,10):
            outFile.write(board[i][j])
        outFile.write("\n")

def battle(port, board, record): # i.e. the host server
    host = sc.gethostname() # retreives the name of the local machine
    ships_sunk = 0
    socket = sc.socket()
    socket.bind((host,port)) # connect host ip and desired port number
    
    while True:
        socket.listen(1) # waits for connection
        player, address = socket.accept()
        
        cords = player.recv(1024).decode()
        print('\nReceived: '+str(cords)+'\n')

        own_out = open("own_board.txt", "w")
        opponent_out = open("opponent_board.txt", "w")
        
        while True:
    
            #parce cords,BAD REQUEST?
            try:
                x = int(cords[6])
                y = int(cords[10])
            except:
                #return bad request
                player.send(('400').encode())
                break
           
            #bounds?    
            if(0>x or x>9)and(0>y or y>9) and cords[7]!=0 and len(cords)<=11:
                #return out of bounds
                player.send(('404').encode())
                break

            #already hit?    
            if(board[x][y]=='X') or (board[x][y]=='O'):
                #return out of bounds
                player.send(('410').encode())
                break
            
            elif(board[x][y]!='_'):
                #hit
                curr = board[x][y]
                board[x][y] = 'X'
                record[x][y] = 'X'
                writeOut(opponent_out, record)
                
                if curr in board:
                    player.send(('200 hit=1').encode())
                    
                else:
                    #sunk
                    player.send(('200 hit=1\&sink='+curr).encode())
                    ships_sunk += 1
                
            else: #miss
                board[x][y] = 'O'
                record[x][y] = 'O'
                
                #return miss
                writeOut(opponent_out, record)
                player.send(('200 hit=0').encode())
                break
                
            #close inner loop
            break

        #close connection
        player.close()

        if(ships_sunk == 5):
            for i in range(0,10):
                for j in range(0,10):
                    own_out.write(board[i][j])
            break

def prepBoard(boardFile):
    file = []
    newFile = []
    for i in range(0,10):
        for j in range (0,10):
            newFile.append(boardFile[i][j])

        file.append(newFile)
        newFile = []
        
    return file

def display(board):
    print('\n  0 1 2 3 4 5 6 7 8 9')
    for i in range(0,10):
        print(str(i)+' '+str(' '.join(board[i])))

#main
if __name__ == '__main__':    
    with open(sys.argv[2]) as f:
        own_board = f.read().splitlines()
    own_board = prepBoard(own_board)
    opponent_board = [['_']*10 for i in range(10)]

    display(own_board)
    display(opponent_board)
    
    port = int(sys.argv[1])
    
    battle(port,own_board,opponent_board)
    
#########################################################################################################
# References:                                                           `                               #
#   https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a   #
#   https://stackoverflow.com/questions/21233340/sending-string-via-socket-python                       #
#########################################################################################################
