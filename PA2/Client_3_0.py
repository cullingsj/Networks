import argparse
import rdt_3_0 as RDT
import time

if __name__ == '__main__':
    parser =  argparse.ArgumentParser(description='Quotation client talking to a Pig Latin server.')
    parser.add_argument('server', help='Server.')
    parser.add_argument('port', help='Port.', type=int)
    args = parser.parse_args()
    
    msg_L = ['The use of COBOL cripples the mind; its teaching should, therefore, be regarded as a criminal offense. -- Edsgar Dijkstra',
            'C makes it easy to shoot yourself in the foot; C++ makes it harder, but when you do, it blows away your whole leg. -- Bjarne Stroustrup',
            'A mathematician is a device for turning coffee into theorems. -- Paul Erdos',
            'Grove giveth and Gates taketh away. -- Bob Metcalfe (inventor of Ethernet) on the trend of hardware speedups not being able to keep up with software demands',
            'Wise men make proverbs, but fools repeat them. -- Samuel Palmer (1805-80)']
    
     
    timeout = 2 #send the next message if no response
    time_of_last_data = time.time()
     
    rdt = RDT.RDT('client', args.server, args.port)
    for i in range(0,5):
        msg_S = msg_L[i]
        rdt.rdt_3_0_send(msg_S)
        recPkt = ['']
        # try to receive message before timeout 
        msg_In = None
        while msg_In == None:
            msg_In = rdt.rdt_3_0_receive()
            
            if msg_In is None:
                if time_of_last_data + timeout < time.time():
                    print("<< Packet timeout resending >>")
                    i = i-1
                else:
                    continue
             
            time_of_last_data = time.time()
            
            if(msg_In and msg_In[:3] == 'NAK'):
                print("NAK RECEIVED FOR: \n"+msg_S+"\n")
                i = i-1
        
            #print the result
            if(msg_In):
                #recPkt.append(msg_In)
                print("ACK RECEIVED FOR: ")
                print('Converting: '+msg_S)
                print('to: '+msg_In[6:]+'\n')
        
    rdt.disconnect()
