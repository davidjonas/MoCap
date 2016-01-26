from abc import ABCMeta, abstractmethod
from datetime import datetime

class ReaderNotAttachedException(Exception):
    pass

class NatNetWriter(object):
    """
    Abstract class that writes MoCap data to a output (live streaming through network or recording to a file)
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        self.startTime = None
        self.writtenFrames = 0
        self.isRunning = False
        self.reader = None

    def attachReader(self, reader):
        self.reader = reader

    def updateHandler(self):
        t = datetime.now()
        dt = (t-self.startTime).total_seconds()

        self.writeDataFrame(self.reader, dt)

    def start(self):
        if self.reader is not None:
            self.openStream()
            self.isRunning = True
            self.startTime = datetime.now()
            self.reader.onUpdate += self.updateHandler
        else:
            raise ReaderNotAttachedException("Cannot start the writer without a reader attached.")

    def stop(self):
        self.isRunning = False
        self.reader.onUpdate -= self.updateHandler
        self.startTime = None
        self.closeStream()

    @abstractmethod
    def openStream(self): pass

    @abstractmethod
    def closeStream(self): pass

    @abstractmethod
    def writeDataFrame(self, reader, timestamp): pass
