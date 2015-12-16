from abc import ABCMeta, abstractmethod
from event import Event
import threading
from datetime import datetime

class NatNetReader(threading.Thread):
    """
    Abstract class that reads MoCap data from an input (live NatNet data or recorded file data)
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.rigidbodies = []
        self.onUpdate = Event()
        self.startTime = None
        self.kill = False
        self.daemon = True

    def countSkeletons(self):
        return len(self.skeletons)

    def countRigidbodies(self):
        return len(self.rigidbodies)

    def getSkeleton(self, index):
        if index > -1 and index < self.countSkeletons():
            return skeletons[index]
        else:
            return None

    def getRigidbody(self, index):
        if index > -1 and index < self.countRigidbodies():
            return self.rigidbodies[index]
        else:
            return None

    def run(self):
        self.startTime = datetime.now()
        self.kill = False
        while not self.kill:
            frame = self.readDataFrame();
            if frame is not None:
                self.onUpdate();
        closeStream();

    def stop(self):
        self.kill = True

    @abstractmethod
    def readDataFrame(self):

    @abstractmethod
    def openStream(self): pass

    @abstractmethod
    def closeStream(self): pass
