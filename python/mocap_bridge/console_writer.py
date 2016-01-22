# This class is mostly for debugging and testing

from terminal_colors import bcolors
from natnet_writer import NatNetWriter

class ConsoleWriter(NatNetWriter):

    def __init__(self, delay=0.5):
        # params
        self.delay=delay
        # attributes
        self.lastTime = None

    def openStream(self): pass

    def closeStream(self): pass

    def writeDataFrame(self, reader, timestamp):
        if self.delay != None and self.lastTime != None and reader.getTime() < (self.lastTime + self.delay):
            return

        line = "{0}: {1} rigid bodies and {2} skeletons".format(reader.getTime(), len(reader.rigidbodies), len(reader.skeletons))
        print(line)
        self.lastTime = reader.getTime()
