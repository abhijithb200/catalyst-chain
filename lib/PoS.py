import random
import datetime
import hashlib

# from state_trie import StateTree
from lib.state_trie import StateTree

m = StateTree()

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

    def create_block(peer,slot):
        block = {'header':
                    {
                    'index': slot,
                    'timestamp': str(datetime.datetime.now()),
                    'mined_by':peer.sport,
                    'hash':0,
                    'previous_hash': peer.chain[-1]['header']['hash'],
                    'stateRoot':m.root.hash
                    },
                 'validated':[peer.sport],
                 'body':None
                }
        block['header']['hash']=hashlib.sha3_256(str(block['header']).encode()).hexdigest()
        
        mempool=[]
        if len(peer.mempool)>0:
            for i in peer.mempool:
                if Block.checkvalidity(i):
                    mempool.append(i)

            block['body'] = mempool
            block['header']['stateRoot']=m.root.hash
        return block

    def checkvalidity(tnx):

        #need to work on nonce later
        try:
            history_from = m.getdata(tnx['from'])
            if int(history_from['balance'])>= int(tnx['amount']):

                try:
                    history_to = m.getdata(tnx['to'])

                    m.replace(tnx['from'],balance=(history_from['balance']-tnx['amount']),nonce=int(history_from['nonce']+1))
                    print(m.root.hash)

                    m.replace(tnx['to'],balance=(int(history_to['balance'])+int(tnx['amount'])),nonce=int(history_to['nonce']+1))

                    print(m.getdata(tnx['from']))
                    print(m.getdata(tnx['to']))
                    print(m.root.hash)
                except KeyError:
                    m.add_leaf(tnx['to'],{'addr':tnx['to'],'nonce':0,'balance':0})                    
                    return Block.checkvalidity(tnx)
                
                return True
            else:
                return False
        except KeyError:
            m.add_leaf(tnx['from'],{'addr':tnx['from'],'nonce':0,'balance':0})
            return Block.checkvalidity(tnx)



# if __name__ == "__main__":
#     tnx = {'from':'0x42D63EA9FFF6896C1D25C98B65461C4bC5C05475','to':'200','nonce':0,'amount':9}
#     # # m.add_leaf(tnx['from'],{'addr':tnx['from'],'nonce':0,'balance':10000000000000000000})
#     # # m.add_leaf(tnx['to'],{'addr':tnx['to'],'nonce':0,'balance':100000000000000000000})
#     while True:
#         input('>')
#         print(Block.checkvalidity(tnx))
#     print(m.getdata('B'))
#     # print(m.root.hash)

    