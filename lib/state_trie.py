from audioop import add
import eth_keys, os
from hashlib import sha3_256
from sqlitedict import SqliteDict


'''
As the transactions happens, each account is updated along with the state root hash
'''





class StateNode:
    def __init__(self,hash):
        self.hash = hash
        self.parent = None
        self.left_child = None
        self.right_child = None
        

class StateTree:
    def __init__(self,db):
        self.leaves = []
        self.db = db
        # self.root = StateNode(self.compute_hash('00'))

    def add_leaf_from_db(self):
        self.leaves = []
        for key, item in self.db.items():
            node = StateNode(self.compute_hash(item))
            self.leaves.append(node)
            self.root = self.build_merkle_tree(self.leaves)

    def add_leaf_to_db(self,addr,value):
        self.db[self.compute_hash(addr)] = value
        

    def build_merkle_tree(self, leaves):
        num_leaves = len(leaves)
        if num_leaves == 1:
            return leaves[0]

        parents = []

        i = 0
        while i < num_leaves:
            left_child = leaves[i]
            right_child = leaves[i + 1] if i + 1 < num_leaves else left_child

            
            parents.append(self.create_parent(left_child, right_child))

            i += 2
        return self.build_merkle_tree(parents)

    def create_parent(self, left_child, right_child):
        parent = StateNode(
            self.compute_hash(left_child.hash + right_child.hash))

        parent.left_child, parent.right_child = left_child, right_child
        left_child.parent, right_child.parent = parent, parent
        return parent

    def replace(self,addr,balance,nonce):
        
        try:
            status = self.getdata(addr)
            self.db[self.compute_hash(addr)] = {'addr':addr,'nonce':nonce,'balance':balance}
        except KeyError:
            print('not found')

        
    def getdata(self,addr):
        return self.db[self.compute_hash(addr)]

    @staticmethod
    def compute_hash(data):
        data = str(data).encode('utf-8')
        return sha3_256(data).hexdigest()
        # return str(data)



if __name__ == "__main__":
    db = SqliteDict("C:/Users/abhij/Desktop/eth-pos-attack/ex.sqlite",autocommit=True)

    m = StateTree(db)

    # #create a new account
    # m.add_leaf("0",{'addr':0,'nonce':0,'balance':1000})
    # m.add_leaf("1",{'addr':1,'nonce':0,'balance':1000})
    # print('hash',m.root.hash)
    # m.add_leaf_to_db("1",{'addr':1,'nonce':0,'balance':100000000})
    m.add_leaf_from_db()


    # print(m.leaves)
    # m.replace("3",balance=800,nonce=1)
    print('hash',m.root.hash)
    # # print(m.root.hash)
    # # print(m.replace("2",balance=1800,nonce=1))
    # print(m.replace("2",balance=2800,nonce=1))
    # # print(m.replace("2",balance=3800,nonce=1))
    # m.replace("2",balance=4800,nonce=1)
    # print('hash',m.root.hash)
    # # print(m.getdata("2"))
    for key, item in db.items():
        print("%s=%s" % (key, item))
    


