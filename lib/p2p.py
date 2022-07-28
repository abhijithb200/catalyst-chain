import socket
import threading
import json

class Peer2Peer:
    def __init__(self):
        self.connections = []
        
    
    def listener(self,port):
        receiver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        receiver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        receiver.bind(('127.0.0.1',int(port)))
        receiver.listen(5)
        print('Listening...',port)

        while True:
            c,addr = receiver.accept()
            self.connections.append(c)
            thre = threading.Thread(target=self.server_handler, args=(c,addr))
            thre.start()
            
    def broadcast(self,msg):
        for i,conn in enumerate(self.connections):
            try:
                conn.send(msg.encode('utf-8'))
            except:
                del self.connections[i]
                print('deleted')
                continue

    def server_handler(self,c,addr):
        while True:
            try:
                print(addr,' : ',c.recv(1024).decode("utf-8"))
            except:
                pass
            msg = input(">")
            self.broadcast(msg)
           
    def start_threat(self,port):
        listener = threading.Thread(target=self.listener,daemon=True,args=(port,))
        listener.start()

    def start_sender_threat(self,port):
        listener = threading.Thread(target=self.sender,daemon=True,args=(port,))
        listener.start()

    def sender(self,port):
        sender = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sender.connect((('127.0.0.1',port)))
        while True:
            try:
                sender.send('hi'.encode('utf-8'))
                data = sender.recv(1024).decode("utf-8")
                print(data)
            except:
                pass
            if len(self.connections)>0:
                self.broadcast(data)
            

class NodeDiscovery(Peer2Peer):
    def __init__(self):
        Peer2Peer.__init__(self)

    def start_udp_threat(self,port):
        listener = threading.Thread(target=self.listen_udp,daemon=True,args=(port,))
        listener.start()

    def send_udp(self,data,port):
        if type(data)==dict:data = json.dumps(data)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.sendto(data.encode(),('127.0.0.1',int(port)))

    def listen_udp(self,port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', int(port)))
        print('Listening udp on ',int(port))

        while True:
            data,addr = sock.recvfrom(2024)
            d = json.loads(str(data.decode()))

            if 'query' in d :
                if d['query'] == "node_discovery":
                    ip,port = d['from']['ip'],int(d['from']['port'])
                    self.send_udp({'result':'fine'},int(port))
            else:
                print(d)
            
            
        