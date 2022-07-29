from lib.p2p import Peer2Peer
import sys


peer = Peer2Peer(sys.argv[1])


while True:
    msg = input('>')
    peer.broadcast({"msg":msg})


