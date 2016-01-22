# This class is mostly for debugging and testing

from terminal_colors import bcolors
from natnet_writer import NatNetWriter

class ConsoleWriter(NatNetWriter):

    def openStream(self): pass

    def closeStream(self): pass

    def writeDataFrame(self, reader, timestamp):
        line = "{0}: {1} rigid bodies and {2} skeletons".format(reader.getTime(), len(reader.rigidbodies), len(reader.skeletons))
        print(line)
