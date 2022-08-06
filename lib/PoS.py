import random
import datetime
import hashlib

class Block:

    @classmethod
    def startchain(cls,peer):
        cls.peer = peer
        peer.chain=[{'header':
                    {
                    'index': 0,
                    'timestamp': str(datetime.datetime.now()),
                    'mined_by' : None,
                    'hash':'0000000000000000000000000000000000000000000000000000000000000000',
                    'previous_hash': 0,
                    'slot':None
                    },
                 'validated':[],
                 'body':None
                }]
        return peer

    def find_proposer(lst):
        if len(lst)==0:
            return 'Noting'
        else:
            selected = random.choice(lst)
            while selected == ('127.0.0.1',5000):
                selected = random.choice(lst)
        
        return selected

    def create_block(peer):
        block = {'header':
                    {
                    'index': 0,
                    'timestamp': str(datetime.datetime.now()),
                    'mined_by':peer.sport,
                    'hash':0,
                    'previous_hash': peer.chain[-1]['header']['hash'],
                    },
                 'validated':[peer.sport],
                 'body':None
                }
        block['header']['hash']=hashlib.sha3_256(str(block['header']).encode()).hexdigest()
        
        return block


