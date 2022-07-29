from multiprocessing import connection
from lib.p2p import Peer2Peer,NodeDiscovery
import socket
import sys


peer = NodeDiscovery()
peer.start_threat(sys.argv[1])
peer.start_udp_threat(sys.argv[1])


if len( sys.argv ) > 2:
    data = {'query':'node_discovery',
            'from':{'ip':'127.0.0.1','port':sys.argv[1]}
            }
            
    peer.send_udp(data,int(sys.argv[2]))
    peer.start_sender_threat(int(sys.argv[2]))
while True:
    pass

# stat = input("Are you ready??")
# if stat=="y":
#     # neigh = [int(sys.argv[2]),int(sys.argv[3])]
#     # connection = []

#     # for i in neigh:
#     #     connection.append(Peer2Peer.sender(i))
#     if len( sys.argv ) > 2:
#         peer.start_sender_threat(int(sys.argv[2]))

#     while True:
#         pass
        # msg = input('Enter something >')

        # for i in connection:
        #     i.send(msg.encode('utf-8'))
        # print(i.recv(1024).decode("utf-8"))

    