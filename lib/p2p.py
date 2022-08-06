import socket
import threading
import json
from lib.slot import Slot
from lib.PoS import Block


class Peer2Peer():
    def __init__(self,sport):
        self.sport = sport
        self.connections = []
        self.mempool = []
        
        #run up the server
        self.start_threat()
        self.querynodestart()
        
    def start_threat(self):
        listener = threading.Thread(target=self.listen,daemon=True,args=(self.sport,))
        listener.start()
        
    def send(data,addr):
        if type(data)==dict:data = json.dumps(data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.sendto(data.encode(),addr)
        
    def broadcast(self,data):
        self.querynodes()
        if type(data)==dict:data = json.dumps(data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(self.connections)
        for i in self.connections:
            if i[1]!=int(self.sport):
                sock.sendto(data.encode(),i)

    def addconnections(self,addr):
        if addr not in self.connections:
            self.connections.append(addr)

    def setconnections(self,d):
        temp = []
        for i in  d:
            temp.append(tuple(i))
        self.connections = temp

    def cast_vote(self):
        vote={'by':self.sport,'slot':Slot.get_slot()}
        self.broadcast(vote)
        
    def querynodes(self):
        data = {'query':'node_discovery',
            'from':{'ip':'127.0.0.1','port':self.sport}
            }

        if self.sport!='5000':
            Peer2Peer.send(data,('127.0.0.1',5000))

    def querynodestart(self):
        data = {'query':'node_start',
            'from':{'ip':'127.0.0.1','port':self.sport}
            }

        if self.sport!='5000':
            Peer2Peer.send(data,('127.0.0.1',5000))
        else:
            self.connections.append(('127.0.0.1',5000))

    def listen(self,port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', int(port)))
        print('Listening udp on ',int(port))

        while True:
            data,addr = sock.recvfrom(2024)
            d = json.loads(str(data.decode()))
            if 'query' in d :
                if d['query'] == "node_discovery":
                    addr = (d['from']['ip'],int(d['from']['port']))
                    self.addconnections(addr)
                    self.broadcast({'nodes':self.connections})

                elif d['query'] == "node_start":
                    addr = (d['from']['ip'],int(d['from']['port']))
                    self.addconnections(addr)
                    self.broadcast({'nodes':self.connections,'slot':Slot.get_slot()})

                
            elif 'nodes' in d:
                self.setconnections(d['nodes'])
                if 'slot' in d:
                    Slot.slotcount = int(d['slot'][0])
                    Slot.second = int(d['slot'][1])
                
            elif 'validator' in d:
                if d['validator'][1] == int(self.sport):
                    print("[!]I am the validator")

                    self.validator = int(self.sport)
                    self.block =  Block.create_block(self,Slot.get_slot()[0])

                    #crate block if i am the validator
                    self.broadcast(self.block)

                    self.mempool = []

            elif 'header' in d:
                self.block = d
                self.block['validated'].append(self.sport)
                
                self.mempool = []
                self.cast_vote()
                

                    
            elif 'by' in d:
                if hasattr(self,'block'): 
                    try:
                        self.block['validated'].append(d['by'])
                        if len(self.block['validated'])==int(len(self.connections)):
                            self.chain.append(self.block)
                            self.block = {}
                            print('[!]Chain Created')
                            print(json.dumps(self.chain, indent=4))
                    except:
                        pass

            elif 'nonce' in d:
                d['nonced'] = d['nonce']
                del d['nonce']
                self.broadcast(d)
                self.mempool.append(d)

            elif 'nonced' in d:
                self.mempool.append(d)

            else:
                print(d)
