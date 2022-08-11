from re import T
import sched, time
import threading
from lib.PoS import Block

class Slot:
    s = sched.scheduler(time.time, time.sleep)
    slotcount = 0
    second = 20
    

    def slotfun(cls,sc):
        if cls.second==20:
            cls.slotcount+=1
            cls.second=0    
            cls.peer.block=={}
        elif cls.second==10 and cls.peer.block=={}:
            #if no block were found upvote the previous block
            cls.peer.cast_vote()

        cls.second+=1
        if cls.peer.sport == 5000 and cls.second==2:
            validator = Block.find_proposer(cls.peer.connections)
            cls.peer.broadcast({"validator":validator})

            

        print("Slot=>",cls.slotcount," ",cls.second,end="\r")
        sc.enter(1, 1,cls.slotfun, (cls,sc,))

    def shoot(cls):
        cls.s.enter(0, 1, cls.slotfun, (cls,cls.s,))
        cls.s.run()

    @classmethod
    def start_slot(cls,peer):
        cls.peer = peer
        listener = threading.Thread(target=cls.shoot,args=(cls,),daemon=True)
        listener.start()

    @classmethod
    def get_slot(cls):
        return cls.slotcount,cls.second

