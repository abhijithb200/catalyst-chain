from lib.crypto import create_key_pair
from lib.p2p import Peer2Peer


# Privkey,Pubkey,Address = create_key_pair()
tnx = {'from':'0x42D63EA9FFF6896C1D25C98B65461C4bC5C05475','to':'B','nonce':0,'amount':80}
Peer2Peer.send(tnx,('127.0.0.5',6000))
