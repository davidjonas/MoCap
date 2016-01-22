from natnet_reader import NatNetReader

class OSCReader(NatNetReader):
    def __init__(self, host="127.0.0.1", port=8080):
        super(OSCReader, self).__init__()

        self.host = host
        self.port = port

        self.osc = None

    def openStream(self):
        if self.osc != None:
            self.closeStream()

        print('TODO: openStream OSC')

    def closeStream(self):
        if self.osc == None:
            return

    def readDataFrame(self):
        if self.osc == None:
            return
