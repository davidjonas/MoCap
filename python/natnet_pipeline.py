# Class that reads data from a NatNetReader and streams it to a NatNetWriter

class NatNetPipeline(object):
    def __init__(self, reader, writer):
        self.reader = reader
        self.writer = writer
        self.writer.attachReader(reader)

    def start(self):
        self.writer.start()
        self.reader.start()
        self.reader.updateRigidbody += self.updateRigidbody

    def stop(self):
        self.reader.stop()
        self.writer.stop()

    def updateRigidbody(self, obj):
        self.writer.writeRigidbody(obj)
