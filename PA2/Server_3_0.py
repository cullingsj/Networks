import argparse
import rdt_3_0 as RDT
import time

def makePigLatin(word):
    m  = len(word)
    vowels = "a", "e", "i", "o", "u", "y" 
    if m<3 or word=="the":
        return word
    else:
        for i in vowels:
            if word.find(i) < m and word.find(i) != -1:
                m = word.find(i)
        if m==0:
            return word+"way" 
        else:
            return word[m:]+word[:m]+"ay" 

def piglatinize(message):
    essagemay = ""
    message = message.strip(".")
    for word in message.split(' '):
        essagemay += " "+makePigLatin(word)
    return essagemay.strip()+"."


if __name__ == '__main__':
    parser =  argparse.ArgumentParser(description='Pig Latin conversion server.')
    parser.add_argument('port', help='Port.', type=int)
    args = parser.parse_args()
    runs = 0
    
    timeout = 5 #close connection if no new data within 5 seconds
    time_of_last_data = time.time()
    rep_msg_S = None
    rdt = RDT.RDT('server', None, args.port)
    while(True):
        #try to receiver message before timeout
        msg_S = rdt.rdt_3_0_receive()
        if msg_S == None and runs >= 5:
            break
        
        if msg_S is None:
            if time_of_last_data + timeout < time.time():
                print("<< Packet timeout resending >>")
                rdt.rdt_3_0_send(rep_msg_S)
            
            else:
                continue
        time_of_last_data = time.time()

        #convert and reply
        if (msg_S and msg_S[:3] == 'NAK'):
            print("<< NAK received >>")
            rdt.rdt_3_0_send('NAK')
        
        elif (msg_S):
            print("SENDING ACK\n")
            #recPkts.append(msg_S)
            rep_msg_S = 'ACK '+piglatinize(msg_S)
            print('Converted %s \nto \n%s\n' % (msg_S, rep_msg_S[3:]))
            rdt.rdt_3_0_send(rep_msg_S)
            runs += 1
                
            
        
    rdt.disconnect()

    
    
    
