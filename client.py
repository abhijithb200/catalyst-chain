from lib.crypto import create_key_pair
from lib.p2p import Peer2Peer


# Privkey,Pubkey,Address = create_key_pair()
tnx = {'from':'1','to':'A','nonce':0,'amount':10}
Peer2Peer.send(tnx,('192.168.1.7',6000))
