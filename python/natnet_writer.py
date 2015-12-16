from abc import ABCMeta, abstractmethod
from datetime import datetime

class NatNetWriter(object):
    """
    Abstract class that writes MoCap data to a output (live streaming through network or recording to a file)
    """
    __metaclass__ = ABCMeta

    def __init__(self, reader):
        self.startTime = None
        self.writtenFrames = 0
        self.isRunning = False
        self.reader = reader

    def updateHandler():
        t = datetime.now()
        dt = (t-self.startTime).total_seconds()

        self.writeDataFrame(self.reader.rigidbodies, dt)

    def start(self):
        self.openStream()
        self.isRunning = True
        self.startTime = datetime.now()
        self.reader.onUpdate += self.updateHandler

    def stop(self):
        self.isRunning = False
        self.reader.onUpdate -= self.updateHandler
        self.startTime = None
        self.closeStream()

    @abstractmethod
    def writeDataFrame(self, rigidbodies, timestamp): pass

    @abstractmethod
    def openStream(self): pass

    @abstractmethod
    def closeStream(self): pass
