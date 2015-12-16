# Class that reads data from a NatNetReader and streams it to a NatNetWriter

class NatNetPipeline(object):
    def __init__(self):
        self.readers = []
        self.writers = []

    def addReader(reader):
        self.readers.append(reader)

    def addWriter(writer):
        self.writers.append(writer)

    
