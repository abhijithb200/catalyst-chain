import socket
import threading


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
            

class NodeDiscovery:
    def __init__(self):
        pass

    def start_threat(self):
        listener = threading.Thread(target=self.listen,daemon=True)
        listener.start()

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', self.sport))
        print('Listening on ',self.sport)

        while True:
            data,addr = sock.recvfrom(2024)
            print(data)
        