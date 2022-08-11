from lib.crypto import create_key_pair
from lib.p2p import Peer2Peer


# Privkey,Pubkey,Address = create_key_pair()
tnx = {'from':'1','to':'A','nonce':0,'amount':10}
Peer2Peer.send(tnx,('13.127.160.25',6000))
