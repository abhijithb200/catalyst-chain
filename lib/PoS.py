import random
import datetime
import hashlib




class Block:

    @classmethod
    def startchain(cls,peer,m):
        cls.peer = peer
        cls.m = m
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


    @classmethod
    def create_block(cls,peer,slot):
        block = {'header':
                    {
                    'index': slot,
                    'timestamp': str(datetime.datetime.now()),
                    'mined_by':peer.sport,
                    'hash':0,
                    'previous_hash': peer.chain[-1]['header']['hash'],
                    'stateRoot':cls.m.root.hash
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
            block['header']['stateRoot']=cls.m.root.hash
        return block

    @classmethod
    def checkvalidity(cls,tnx):

        #need to work on nonce later
        try:
            history_from = cls.m.getdata(tnx['from'])
            if int(history_from['balance'])>= int(tnx['amount']):

                try:
                    history_to = cls.m.getdata(tnx['to'])

                    cls.m.replace(tnx['from'],balance=(int(history_from['balance'])-int(tnx['amount'])),nonce=int(history_from['nonce']+1))
                    cls.m.replace(tnx['to'],balance=(int(history_to['balance'])+int(tnx['amount'])),nonce=int(history_to['nonce']+1))
                    cls.m.add_leaf_from_db()
                    print(cls.m.root.hash)
                except KeyError:
                    cls.m.add_leaf_to_db(tnx['to'],{'addr':tnx['to'],'nonce':0,'balance':0}) 
                    cls.m.add_leaf_from_db()                   
                    return Block.checkvalidity(tnx)
                
                return True
            else:
                return False
        except KeyError:
            cls.m.add_leaf_to_db(tnx['from'],{'addr':tnx['from'],'nonce':0,'balance':0})
            cls.m.add_leaf_from_db()
            return Block.checkvalidity(tnx)



if __name__ == "__main__":
    tnx = {'from':'1','to':'200','nonce':0,'amount':9}
    # # cls.m.add_leaf(tnx['from'],{'addr':tnx['from'],'nonce':0,'balance':10000000000000000000})
    # # cls.m.add_leaf(tnx['to'],{'addr':tnx['to'],'nonce':0,'balance':100000000000000000000})
    while True:
        input('>')
        print(Block.checkvalidity(tnx))
    print(cls.m.getdata('B'))
    # print(cls.m.root.hash)

    