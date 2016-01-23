from mocap_bridge.utils.color_terminal import ColorTerminal
from mocap_bridge.utils.event import Event
from mocap_bridge.interface.rigid_body import RigidBody # Skeleton not yet supported
from datetime import datetime

try:
    import OSC
except ImportError:
    print ColorTerminal().fail("Error importing library, please install pyOSC by running: sudo pip install pyOSC")

import threading

class OscReader:
    def __init__(self, host="127.0.0.1", port=8080, manager=None, threaded=False):
        # params
        self.manager = manager
        self.host = host
        self.port = port
        self.threaded = threaded

        # attrs
        self.oscServer = None
        self.startTime = None
        self.thread = None

        # events
        self.onUpdate = Event()

    def start(self):
        if not self.threaded:
            self.setup()
            return

        if self.thread:
            ColorTerminal().warn("OscReader - Can't start while a htread is already running")
            return

        self._kill = False
        # threaded loop method will call setup
        self.thread = threading.Thread(target=self.threaded_loop)

    def stop(self):
        if self.threaded:
            # threaded loop method will call destroy
            self._kill = True
        else:
            self.destroy()

    def setup(self):
        print 'setup'
        if self.oscServer != None:
            self.destroy()

        ColorTerminal().output("Starting OSC server with host {0} and port {1}".format(self.host, self.port))
        self.oscServer = OSC.OSCServer((self.host, self.port))
        self.oscServer.handle_timeout = self.handleTimeout
        self.oscServer.addMsgHandler('/rigidbody', self.oscRigidBodyHandler)
        ColorTerminal().success("Server running")

        self.startTime = datetime.now()

    def destroy(self):
        if self.oscServer == None:
            return

        self.oscServer.close()
        self.oscServer = None

    def threaded_loop(self):
        self.setup()

        while not self._kill:
            self.update()

        self.destroy()

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

    def getTime(self):
        if self.startTime is None:
            return 0

        return (datetime.now()-self.startTime).total_seconds()

    def oscRigidBodyHandler(self, addr, tags, data, client_address):
        # readers can interface with the mocap data manager directly (most efficient)
        rb = RigidBody().fromJSON(data[0])

        if self.manager:
            self.manager.addOrUpdateRigidBody(rb)

        self.onRigidBody(rb)

    def handleTimeout(self):
        if self.oscServer != None:
            self.oscServer.timed_out = True
