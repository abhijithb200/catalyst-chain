#https://pymerkle.readthedocs.io/en/latest/proof.html#verification
from hashlib import sha3_256

'''
Collect all the transaction and create a merkle tree from that where we can do proof and all
'''

class MerkleNode:
    def __init__(self,hash):
        self.hash = hash
        self.parent = None
        self.left_child = None
        self.right_child = None
        

class MerkleTree:
    def __init__(self,data_chunks):
        self.leaves = []

        for chunk in data_chunks:
            node = MerkleNode(self.compute_hash(chunk))
            self.leaves.append(node)

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
        parent = MerkleNode(
            self.compute_hash(left_child.hash + right_child.hash))

        parent.left_child, parent.right_child = left_child, right_child
        left_child.parent, right_child.parent = parent, parent

        return parent
        
    def get_audit_trail(self,chunk_hash):
        for leaf in self.leaves:
            if leaf.hash == chunk_hash:
                print("Leaf exists")
                return self.generate_audit_trial(leaf)
        return False

    def generate_audit_trial(self,merkle_node,trail=[]):
        if merkle_node == self.root:
            trail.append(merkle_node.hash)
            return trail

        is_left = merkle_node.parent.left_child == merkle_node
        print(is_left)
        if is_left: 
            trail.append((merkle_node.parent.right_child.hash, False))
            return self.generate_audit_trial(merkle_node.parent, trail)
        else:
            trail.append((merkle_node.parent.left_child.hash, True))
            return self.generate_audit_trial(merkle_node.parent, trail)

    

    def verify_audit_trail(chunk_hash,audit_trail):
        proof_till_now = chunk_hash

        for node in audit_trail[:-1]:
            hash = node[0]
            is_left = node[1]

            if is_left:
                proof_till_now = MerkleTree.compute_hash(hash + proof_till_now)
            else:
                proof_till_now = MerkleTree.compute_hash(proof_till_now + hash)


            print(proof_till_now)

        return proof_till_now == audit_trail[-1]


    @staticmethod
    def compute_hash(data):
        data = str(data).encode('utf-8')
        return sha3_256(data).hexdigest()

chunks = [{'name':'Abhijith','class':1},{'name':'Abhijith','class':2},{'name':'Abhijith','class':3}]
m = MerkleTree(chunks)

print('Root Hash :',m.root.hash)

chunk_hash = MerkleTree.compute_hash({'name':'Abhijith','class':1})
print('Chunk hash :',chunk_hash)
audit = m.get_audit_trail(chunk_hash)

print(audit)

print(MerkleTree.verify_audit_trail(chunk_hash,audit))