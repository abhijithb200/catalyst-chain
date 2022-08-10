import threading
from lib.p2p import Peer2Peer
import sys
from lib.slot import Slot
from lib.PoS import Block
from lib.state_trie import StateTree
from sqlitedict import SqliteDict



db = SqliteDict("ex.sqlite",autocommit=True)
# db['67b176705b46206614219f47a05aee7ae6a3edbe850bbbe214c536b989aea4d2'] = {'addr':'1','nonce':0,'balance':100000000}


m = StateTree(db)
m.add_leaf_from_db()

peer = Peer2Peer(sys.argv[1])

Slot.start_slot(peer)


#create the genesis block
Block.startchain(peer,m)


while True:

    try:
        msg = input('>')
        peer.broadcast({"msg":msg})

    except KeyboardInterrupt:
        peer.queryend()
        print('exiting...')
        exit()


