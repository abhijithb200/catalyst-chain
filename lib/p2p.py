from http import client
from re import T
import socket
import threading


class Peer2Peer:
    def __init__(self):
        self.connections = []
        print('fuck')
        
    
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
            
    def broadcast(self):
        print(self.connections)
        for i in self.connections:
            i.send("hey".encode('utf-8'))

    def server_handler(self,c,addr):
        while True:
            print(addr,' : ',c.recv(1024).decode("utf-8"))
            self.broadcast()
    def start_threat(self,port):
        listener = threading.Thread(target=self.listener,daemon=True,args=(port,))
        listener.start()

    def sender(self,port):
        sender = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sender.connect((('127.0.0.1',port)))
        while True:
            msg = input(">")
            sender.send(msg.encode('utf-8'))
            print(sender.recv(1024).decode("utf-8"))
        