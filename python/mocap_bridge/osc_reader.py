from color_terminal import ColorTerminal
from natnet_reader import NatNetReader
from natnet_data import RigidBody # Skeleton not yet supported

try:
    import OSC
except ImportError:
    print ColorTerminal().fail("Error importing library, please install pyOSC by running: sudo pip install pyOSC")

import types

class OSCReader(NatNetReader):
    def __init__(self, host="127.0.0.1", port=8080):
        super(OSCReader, self).__init__()
        # params
        self.host = host
        self.port = port
        # attrs
        self.oscServer = None

    def openStream(self):
        if self.oscServer != None:
            self.closeStream()

        ColorTerminal().output("Starting OSC server with host {0} and port {1}".format(self.host, self.port))
        self.oscServer = OSC.OSCServer((self.host, self.port))
        self.oscServer.handle_timeout = self.handleTimeout #types.MethodType(handle_timeout, server)
        self.oscServer.addMsgHandler('/rigidbody', self.oscRigidBodyHandler)
        ColorTerminal().success("Server running")

    def oscRigidBodyHandler(self, addr, tags, data, client_address):
        rb = RigidBody().fromJSON(data[0])
        self.addOrUpdateRigidbody(rb)

    def handleTimeout(self):
        if self.oscServer != None:
            self.oscServer.timed_out = True

    def closeStream(self):
        if self.oscServer == None:
            return

        self.oscServer.close()
        self.oscServer = None

    def readDataFrame(self):
        if self.oscServer == None:
            return

        # # clear timed_out flag
        self.oscServer.timed_out = False
        maxRuns = 10
        runCount = 0
        # # handle all pending requests then return
        while not self.oscServer.timed_out and runCount < maxRuns:
            self.oscServer.handle_request()
            runCount += 1
