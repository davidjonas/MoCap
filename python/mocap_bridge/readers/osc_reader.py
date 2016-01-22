from threaded_reader import ThreadedReader

from mocap_bridge.utils.color_terminal import ColorTerminal
from mocap_bridge.utils.event import Event
from mocap_bridge.interface.rigid_body import RigidBody # Skeleton not yet supported

try:
    import OSC
except ImportError:
    print ColorTerminal().fail("Error importing library, please install pyOSC by running: sudo pip install pyOSC")

class OscReader(ThreadedReader):
    def __init__(self, host="127.0.0.1", port=8080, manager=None):
        super(OscReader, self).__init__(manager)

        # params
        self.host = host
        self.port = port

        # attrs
        self.oscServer = None

        # events
        self.onRigidBody = Event()

    def setup(self):
        if self.oscServer != None:
            self.destroy()

        ColorTerminal().output("Starting OSC server with host {0} and port {1}".format(self.host, self.port))
        self.oscServer = OSC.OSCServer((self.host, self.port))
        self.oscServer.handle_timeout = self.handleTimeout
        self.oscServer.addMsgHandler('/rigidbody', self.oscRigidBodyHandler)
        ColorTerminal().success("Server running")

    def destroy(self):
        if self.oscServer == None:
            return

        self.oscServer.close()
        self.oscServer = None

    def update(self):
        if self.oscServer == None:
            return

        # we'll enforce a limit to the number of osc requests
        # we'll handle in a single iteration, otherwise we might
        # get stuck in processing an endless stream of data
        limit = 10
        count = 0

        # clear timed_out flag
        self.oscServer.timed_out = False

        # handle all pending requests then return
        while not self.oscServer.timed_out and count < limit:
            self.oscServer.handle_request()
            count += 1

    def oscRigidBodyHandler(self, addr, tags, data, client_address):
        # readers can interface with the mocap data manager directly (most efficient)
        rb = RigidBody().fromJSON(data[0])

        if self.manager:
            self.manager.addOrUpdateRigidBody(rb)

        self.onRigidBody(rb)

    def handleTimeout(self):
        if self.oscServer != None:
            self.oscServer.timed_out = True
