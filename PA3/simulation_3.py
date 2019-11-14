'''
Created on Oct 12, 2016

@author: mwittie
'''
import network_3 as network
import link_3 as link
import threading
from time import sleep

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 16 #give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads
    
    #create network nodes
    host_1 = network.Host(1)
    object_L.append(host_1)
    host_2 = network.Host(2)
    object_L.append(host_2)
    
    host_3 = network.Host(3)
    object_L.append(host_3)
    host_4 = network.Host(4)
    object_L.append(host_4)
    
    router_a = network.Router(name='A', intf_count=2, max_queue_size=router_queue_size)
    object_L.append(router_a)
    router_b = network.Router(name='B', intf_count=2, max_queue_size=router_queue_size)
    object_L.append(router_b)
    router_c = network.Router(name='C', intf_count=2, max_queue_size=router_queue_size)
    object_L.append(router_c)
    router_d = network.Router(name='D', intf_count=2, max_queue_size=router_queue_size)
    object_L.append(router_d)
    
    #create a Link Layer to keep track of links between network nodes
    link_layer = link.LinkLayer()
    object_L.append(link_layer)
    
    #add all the links
    #link parameters: from_node, from_intf_num, to_node, to_intf_num, mtu
    link_layer.add_link(link.Link(host_1, 0, router_a, 0, 50))
    link_layer.add_link(link.Link(host_2, 0, router_a, 1, 50))
    
    link_layer.add_link(link.Link(router_a, 0, router_b, 0, 50))
    link_layer.add_link(link.Link(router_a, 1, router_c, 0, 50))
    
    link_layer.add_link(link.Link(router_b, 0, router_d, 0, 50))
    link_layer.add_link(link.Link(router_c, 0, router_d, 1, 50))
    
    link_layer.add_link(link.Link(router_d, 0, host_3, 0, 30))
    link_layer.add_link(link.Link(router_d, 1, host_4, 0, 30))
    
    
    #start all the objects
    thread_L = []
    thread_L.append(threading.Thread(name=host_1.__str__(), target=host_1.run))
    thread_L.append(threading.Thread(name=host_2.__str__(), target=host_2.run))
    thread_L.append(threading.Thread(name=host_3.__str__(), target=host_3.run))
    thread_L.append(threading.Thread(name=host_4.__str__(), target=host_4.run))
    thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))
    thread_L.append(threading.Thread(name=router_b.__str__(), target=router_b.run))
    thread_L.append(threading.Thread(name=router_c.__str__(), target=router_c.run))
    thread_L.append(threading.Thread(name=router_d.__str__(), target=router_d.run))
    
    thread_L.append(threading.Thread(name="Network", target=link_layer.run))
    
    for t in thread_L:
        t.start()
    
    hostMessages = [' I wanna be the very best, like no one e',
                     ' ver was to catch them is my real test..']
    
    #create some send events
    '''for i in range(3):
        host_1.udt_send(2, 'Sample data %d' % i)'''

    for i in range(2):
        host_1.udt_send(i+3, hostMessages[i])

    for i in range(2):
        host_2.udt_send(i+3, hostMessages[i])
    
    
    
    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)
    
    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()
        
    print("All simulation threads joined")



# writes to host periodically
