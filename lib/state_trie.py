from audioop import add
from sqlitedict import SqliteDict
import eth_keys, os
from hashlib import sha3_256


'''
As the transactions happens, each account is updated along with the state root hash
'''

# db = SqliteDict("exams.sqlite")
db = SqliteDict("./lib/ex.sqlite",autocommit=True)




class StateNode:
    def __init__(self,hash):
        self.hash = hash
        self.parent = None
        self.left_child = None
        self.right_child = None
        

class StateTree:
    def __init__(self):
        self.leaves = []
        self.root = StateNode(self.compute_hash('00'))
        for key, item in db.items():
            self.add_leaf(key,item)
        #admin accoount with balance this

    def add_leaf(self,addr,value):
        node = StateNode(self.compute_hash(value))
        self.leaves.append(node)

        db[self.compute_hash(addr)] = value
        self.root = self.build_merkle_tree(self.leaves)


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
        
        for leaf in self.leaves: 
            if leaf.hash == self.compute_hash(db[self.compute_hash(addr)]):
                path = self.generate_path(leaf)
                db[self.compute_hash(addr)] = {'addr':addr,'nonce':nonce,'balance':balance}
                leaf.hash = self.compute_hash(db[self.compute_hash(addr)])
                modi = self.compute_hash((db[self.compute_hash(addr)]))
                self.reproduce(modi,path)





    def reproduce(self,modi,path):
        proof_till_now = modi

        for node in path:
            hash = node[0]
            is_left = node[1]

            if is_left:
                proof_till_now = StateTree.compute_hash(hash+proof_till_now)
            else:
                proof_till_now = StateTree.compute_hash(proof_till_now+hash)

        self.root.hash = proof_till_now 
        

    def generate_path(self,new_leaf,trial=[]):
        if new_leaf == self.root:
            return trial

        is_left = new_leaf.parent.left_child == new_leaf
        if is_left:
            trial.append((new_leaf.parent.right_child.hash,False))
            return self.generate_path(new_leaf.parent,trial)
        else:
            trial.append((new_leaf.parent.left_child.hash,True))
            return self.generate_path(new_leaf.parent,trial)
        
    def getdata(self,addr):
        return db[self.compute_hash(addr)]

    @staticmethod
    def compute_hash(data):
        data = str(data).encode('utf-8')
        return sha3_256(data).hexdigest()
        # return str(data)



if __name__ == "__main__":
    # m = StateTree()

    # #create a new account
    # m.add_leaf("0",{'addr':0,'nonce':0,'balance':1000})
    # m.add_leaf("1",{'addr':1,'nonce':0,'balance':1000})
    # m.add_leaf("2",{'addr':2,'nonce':0,'balance':1000})
    # m.add_leaf("3",{'addr':3,'nonce':0,'balance':1000})

    # # m.replace(str({'addr':2,'nonce':0,'balance':1000}))

    # print(m.root.hash)
    # # m.replace("2",balance=800,nonce=1)
    # # print(m.root.hash)
    # # print(m.replace("2",balance=1800,nonce=1))
    # # print(m.replace("2",balance=2800,nonce=1))
    # # print(m.replace("2",balance=3800,nonce=1))
    # m.replace("2",balance=4800,nonce=1)
    # print(m.root.hash)
    # print(m.getdata("2"))
    for key, item in db.items():
        print("%s=%s" % (key, item))
    


