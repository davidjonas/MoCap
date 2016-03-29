from abc import ABCMeta, abstractmethod
from event import Event
import threading
from datetime import datetime
from natnet_data import *

class NatNetReader(threading.Thread):
    """
    Abstract class that reads MoCap data from an input (live NatNet data or recorded file data)
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        threading.Thread.__init__(self)
        self.rigidbodies = {}
        self.skeletons = {}
        self.onUpdate = Event()
        self.onRigidbodyUpdate = Event()
        self.startTime = None
        self.kill = False
        self.daemon = True

    def countSkeletons(self):
        return len(self.skeletons)

    def countRigidbodies(self):
        return len(self.rigidbodies)

    def getOrCreateSkeleton(self, skelid):
        if skelid in self.skeletons.keys():
            return self.skeletons[skelid]
        else:
            skel = Skeleton(skelid)
            self.skeletons[skelid] = skel
            return skel

    def addOrUpdateRigidbody(self, rb):
        try:
            self.rigidbodies[rb.id].update(rb.position, rb.orientation)
        except:
            self.rigidbodies[rb.id] = rb
        self.onRigidbodyUpdate(rb)

    def getAllRigidbodies(self):
        #return self.rigidbodies
        #TODO: Deal with skeletons here, keep it perfomance critical
        allrb = {}
        for rb in self.rigidbodies.keys():
            allrb[rb] = self.rigidbodies[rb]

        for s in self.skeletons.keys():
            for r in self.skeletons[s].rigidbodies:
                allrb[r] = self.skeletons[s].rigidbodies[r]
        return allrb

    def getTime(self):
        if self.startTime is not None:
            t = datetime.now()
            dt = (t-self.startTime).total_seconds()
            return dt
        else:
            return 0

    def run(self):
        self.openStream()
        self.kill = False
        self.startTime = datetime.now()
        while not self.kill:
            self.readDataFrame()
            self.onUpdate()
        self.closeStream()

    def stop(self):
        self.kill = True

    @abstractmethod
    def openStream(self): pass

    @abstractmethod
    def closeStream(self): pass

    @abstractmethod
    def readDataFrame(self): pass
