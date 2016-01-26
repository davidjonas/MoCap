from abc import ABCMeta, abstractmethod
from event import Event
import threading
from datetime import datetime
from mocap_interface.rigid_body import RigidBody
from mocap_interface.skeleton import Skeleton

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
            self.skeletonsp[skelid] = skel
            return skel

    def addOrUpdateRigidbody(self, rb):
        if rb.id in self.rigidbodies.keys():
            self.rigidbodies[rb.id].update(rb.position, rb.orientation)
        else:
            self.rigidbodies[rb.id] = rb

    def getAllRigidbodies(self):
        return self.rigidbodies
        #TODO: Deal with skeletons here, keep it perfomance critical
        #allrb = []
        #allrb += self.rigidbodies
        #for s in self.skeletons:
        #    allrb += s.rigidbodies
        #return allrb

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
