import queue
import threading


## wrapper class for a queue of packets
class Interface:
    ## @param maxsize - the maximum size of the queue storing packets
    def __init__(self, maxsize=0):
        self.in_queue = queue.Queue(maxsize)
        self.out_queue = queue.Queue(maxsize)

    ##get packet from the queue interface
    # @param in_or_out - use 'in' or 'out' interface
    def get(self, in_or_out):
        try:
            if in_or_out == 'in':
                pkt_S = self.in_queue.get(False)
                # if pkt_S is not None:
                #     print('getting packet from the IN queue')
                return pkt_S
            else:
                pkt_S = self.out_queue.get(False)
                # if pkt_S is not None:
                #     print('getting packet from the OUT queue')
                return pkt_S
        except queue.Empty:
            return None

    ##put the packet into the interface queue
    # @param pkt - Packet to be inserted into the queue
    # @param in_or_out - use 'in' or 'out' interface
    # @param block - if True, block until room in queue, if False may throw queue.Full exception
    def put(self, pkt, in_or_out, block=False):
        if in_or_out == 'out':
            # print('putting packet in the OUT queue')
            self.out_queue.put(pkt, block)
        else:
            # print('putting packet in the IN queue')
            self.in_queue.put(pkt, block)


## Implements a network layer packet.
class NetworkPacket:
    ## packet encoding lengths
    dst_S_length = 5
    prot_S_length = 1

    ##@param dst: address of the destination host
    # @param data_S: packet payload
    # @param prot_S: upper layer protocol for the packet (data, or control)
    def __init__(self, dst, prot_S, data_S):
        self.dst = dst
        self.data_S = data_S
        self.prot_S = prot_S

    ## called when printing the object
    def __str__(self):
        return self.to_byte_S()

    ## convert packet to a byte string for transmission over links
    def to_byte_S(self):
        byte_S = str(self.dst).zfill(self.dst_S_length)
        if self.prot_S == 'data':
            byte_S += '1'
        elif self.prot_S == 'control':
            byte_S += '2'
        else:
            raise ('%s: unknown prot_S option: %s' % (self, self.prot_S))
        byte_S += self.data_S
        return byte_S

    ## extract a packet object from a byte string
    # @param byte_S: byte string representation of the packet
    @classmethod
    def from_byte_S(self, byte_S):
        dst = byte_S[0: NetworkPacket.dst_S_length].strip('0')
        prot_S = byte_S[NetworkPacket.dst_S_length: NetworkPacket.dst_S_length + NetworkPacket.prot_S_length]
        if prot_S == '1':
            prot_S = 'data'
        elif prot_S == '2':
            prot_S = 'control'
        else:
            raise ('%s: unknown prot_S field: %s' % (self, prot_S))
        data_S = byte_S[NetworkPacket.dst_S_length + NetworkPacket.prot_S_length:]
        return self(dst, prot_S, data_S)


## Implements a network host for receiving and transmitting data
class Host:

    ##@param addr: address of this node represented as an integer
    def __init__(self, addr):
        self.addr = addr
        self.intf_L = [Interface()]
        self.stop = False  # for thread termination

    ## called when printing the object
    def __str__(self):
        return self.addr

    ## create a packet and enqueue for transmission
    # @param dst: destination address for the packet
    # @param data_S: data being transmitted to the network layer
    def udt_send(self, dst, data_S):
        p = NetworkPacket(dst, 'data', data_S)
        print('%s: sending packet "%s"' % (self, p))
        self.intf_L[0].put(p.to_byte_S(), 'out')  # send packets always enqueued successfully

    ## receive packet from the network layer
    def udt_receive(self):
        pkt_S = self.intf_L[0].get('in')
        if pkt_S is not None:
            print('%s: received packet "%s"' % (self, pkt_S))

    ## thread target for the host to keep receiving data
    def run(self):
        print(threading.currentThread().getName() + ': Starting')
        while True:
            # receive data arriving to the in interface
            self.udt_receive()
            # terminate
            if (self.stop):
                print(threading.currentThread().getName() + ': Ending')
                return


## Implements a multi-interface router
class Router:

    ##@param name: friendly router name for debugging
    # @param cost_D: cost table to neighbors {neighbor: {interface: cost}}
    # @param max_queue_size: max queue length (passed to Interface)
    def __init__(self, name, cost_D, max_queue_size):
        self.stop = False  # for thread termination
        self.name = name
        # create a list of interfaces
        self.intf_L = [Interface(max_queue_size) for _ in range(len(cost_D))]
        # save neighbors and interfaces on which we connect to them
        self.cost_D = cost_D  # {neighbor: {interface: cost}}
        # TODO: set up the routing table for connected hosts
        self.rt_tbl_D = {name: {name: 0}}  # {destination: {router: cost}}
        self.routers = {name: ''}

        for i in cost_D:
            for entry in cost_D[i]:
                self.rt_tbl_D[i] = {name: cost_D[i][entry]}

        print('%s: Initialized routing table' % self)
        self.print_routes()

    ## Print routing table
    def print_routes(self):
        # TODO: print the routes as a two dimensional table
        if (len(self.rt_tbl_D) > 0):
            print((len(self.rt_tbl_D) * 3 + 4) * '=')
            print("|%s" % self.name, end='')
            for destination in self.rt_tbl_D:
                print("|%s" % destination, end='')

            for name in self.routers:
                print("|\n|%s" % name, end='')
                for destination in self.rt_tbl_D:
                    # print("\nEntry Destination: %s Router: %s" % (destination, name))
                    print("| %s" % self.rt_tbl_D[destination][name], end='')
            print("|\n" + (len(self.rt_tbl_D) * 3 + 4) * '=')
        else:
            print("empty routing table")

    def converge_tables(self, router_in):
        print("converging tables %s and %s" % (self.name, router_in.name))
        self.routers[router_in.name] = ''
        for destination in self.rt_tbl_D:
            if ((router_in.name not in self.rt_tbl_D[destination])):
                temp = {router_in.name: int(router_in.rt_tbl_D[destination][router_in.name])}
                self.rt_tbl_D[destination].update(temp)

    ## called when printing the object
    def __str__(self):
        return self.name

    ## look through the content of incoming interfaces and
    # process data and control packets
    def process_queues(self):
        for i in range(len(self.intf_L)):
            pkt_S = None
            # get packet from interface i
            pkt_S = self.intf_L[i].get('in')
            # if packet exists make a forwarding decision
            if pkt_S is not None:
                p = NetworkPacket.from_byte_S(pkt_S)  # parse a packet out
                if p.prot_S == 'data':
                    self.forward_packet(p, i)
                    ##print('%s: forwarding packet "%s"' % (self, pkt_S))
                elif p.prot_S == 'control':
                    self.update_routes(p, i)
                else:
                    raise Exception('%s: Unknown packet type in packet %s' % (self, p))

    ## forward the packet according to the routing table
    #  @param p Packet to forward
    #  @param i Incoming interface number for packet p
    def forward_packet(self, p, i):
        try:
            # TODO: Here you will need to implement a lookup into the
            # forwarding table to find the appropriate outgoing interface
            # for now we assume the outgoing interface is 1
            lowest = 100
            interface = 1
            dest = p.dst[5 - p.dst_S_length:]
            entrySaved = ''
            # print("Printing dest %s" % p.dst[5-p.dst_S_length:])
            for entry in self.cost_D:
                for face in self.cost_D[entry]:
                    if (not (face == i) and not str(entry)[:1] == 'H'):
                        if (self.rt_tbl_D[dest][entry] < lowest):
                            lowest = self.rt_tbl_D[dest][entry]
                            entrySaved = entry
                            interface = int(face)
            print("Taking interface %d from %s to %s" % (interface, self.name, entrySaved))
            self.intf_L[interface].put(p.to_byte_S(), 'out', True)

            # print('%s: forwarding packet "%s" from interface %d to %d' % \
            #    (self, p, i, 1))
        except queue.Full:
            print('%s: packet "%s" lost on interface %d' % (self, p, i))
            pass

    ## send out route update
    # @param i Interface number on which to send out a routing update
    def send_routes(self, i):
        # TODO: Send out a routing table update
        # create a routing table update packet
        for j in range(len(self.intf_L)):
            if (not (self.name == 'RA' and j == 0) and not (self.name == 'RB' and j == 1)):
                for destination in self.rt_tbl_D:
                    for router in self.rt_tbl_D[destination]:
                        # print("PRINTING SEND_ROUTES PACKET"+str(destination)+self.name+str(self.rt_tbl_D[destination][router]))
                        p = NetworkPacket(0, 'control',
                                          str(destination) + self.name + str(self.rt_tbl_D[destination][router]))
                        try:
                            # print('%s: sending routing update "%s" from interface %d' % (self, p, j))
                            self.intf_L[j].put(p.to_byte_S(), 'out', True)
                        except queue.Full:
                            # print('%s: packet "%s" lost on interface %d' % (self, p, j))
                            pass

    ## forward the packet according to the routing table
    #  @param p Packet containing routing information
    def update_routes(self, p, i):
        # TODO: add logic to update the routing tables and
        # possibly send out routing updates
        data = p.data_S
        change = False
        if (data[:2] == self.name):
            pass
        elif (data[:2] not in self.rt_tbl_D or int(data[4]) < self.rt_tbl_D[data[:2]][self.name]):
            # print("Setting data for %s with cost of %s" % (data[:2], data[4]))
            newCost = int(data[4]) + self.rt_tbl_D[data[2:4]][self.name]
            self.rt_tbl_D[data[:2]] = {self.name: newCost}
            self.rt_tbl_D[data[:2]].update({data[2:4]: int(data[4])})
            self.routers[data[2:4]] = ''
            change = True
        if (change):
            self.send_routes(i)

        # print('%s: Received routing update %s from interface %d' % (self, p, i))

    ## thread target for the host to keep forwarding data
    def run(self):
        print(threading.currentThread().getName() + ': Starting')
        while True:
            self.process_queues()
            if self.stop:
                print(threading.currentThread().getName() + ': Ending')
                return 
