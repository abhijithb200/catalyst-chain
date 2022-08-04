import threading
from lib.p2p import Peer2Peer
import sys
from lib.slot import Slot
from lib.PoS import Block



peer = Peer2Peer(sys.argv[1])
Slot.start_slot(peer)

#create the genesis block
Block.startchain(peer)


while True:
    msg = input('>')
    peer.broadcast({"msg":msg})


