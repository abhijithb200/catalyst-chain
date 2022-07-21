from multiprocessing import connection
from lib.p2p import Peer2Peer
import socket
import sys


peer = Peer2Peer()
peer.start_threat(sys.argv[1])

stat = input("Are you ready??")
if stat=="y":
    # neigh = [int(sys.argv[2]),int(sys.argv[3])]
    # connection = []

    # for i in neigh:
    #     connection.append(Peer2Peer.sender(i))
    if len( sys.argv ) > 2:
        peer.sender(int(sys.argv[2]))

    while True:
        pass
        # msg = input('Enter something >')

        # for i in connection:
        #     i.send(msg.encode('utf-8'))
        # print(i.recv(1024).decode("utf-8"))

    