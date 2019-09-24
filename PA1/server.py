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

def battle(port, board): # i.e. the host server
    host = sc.gethostbyname(sc.gethostname()) # retreives the name of the local machine
    ships_sunk = 0
    socket = sc.socket()
    socket.bind((host,port)) # connect host ip and desired port number
    
    while True:
        socket.listen(1) # waits for connection
        player, address = socket.accept()
        
        cords = player.recv(1024).decode()
        print('\nReceived: '+str(cords)+'\n')
        
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
                player.send(('410').encode())
            
            elif(board[x][y]!='_'):
                #hit
                curr = board[x][y]
                board[x][y] = 'X'
                part_count = 0
                own_out = open("own_board.txt", 'w')
                
                for i in range(0,10):
                    print(''.join(board[i]))
                    own_out.write(''.join(board[i]))
                    own_out.write("\n")
                    for j in range(0,10):
                        if (board[i][j]==curr):
                            part_count += 1
                if(part_count > 0):
                    player.send(('200 hit=1').encode())
                else:
                    #sunk
                    player.send(('200 hit=1\&sink='+curr).encode())
                    ships_sunk += 1
                
            else: #miss
                board[x][y] = 'O'
                own_out = open("own_board.txt", 'w')
                
                for i in range(0,10):
                    print(''.join(board[i]))
                    own_out.write(''.join(board[i]))
                    own_out.write("\n")
                    
                #return miss
                player.send(('200 hit=0').encode())

            

            #close inner loop
            break
            
        #close connection
        player.close()
        
        if(ships_sunk == 5):
            print("\n\n\n\n\n\n\n\n\nYou win!")
            break

def prepBoard(boardFile):
    file = []
    newFile = []
    for i in range(0,10):
        for j in range (0,10):
            newFile.append(boardFile[i][j])

        file.append(newFile)
        newFile = []
        
    display(file)
        
    return file

def display(board):
    print('\n  0 1 2 3 4 5 6 7 8 9')
    for i in range(0,10):
        print(str(i)+' '+str(' '.join(board[i])))

#main
if __name__ == '__main__':    
    with open(sys.argv[2],"r") as f:
        own_board = f.read().splitlines()
        f.close()
    own_board = prepBoard(own_board)
        
    port = int(sys.argv[1])
    
    battle(port,own_board)
    
#########################################################################################################
# References:                                                           `                               #
#   https://medium.com/podiihq/networking-how-to-communicate-between-two-python-programs-abd58b97390a   #
#   https://stackoverflow.com/questions/21233340/sending-string-via-socket-python                       #
#########################################################################################################
