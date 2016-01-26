from mocap_bridge.utils.color_terminal import ColorTerminal

# try:
from OSC import OSCServer
# except ImportError:
#     print(ColorTerminal().fail("Error importing library, please install pyOSC by running: sudo pip install pyOSC"))

import threading

class OscReader:
    def __init__(self, host="127.0.0.1", port=8080, manager=None, threaded=False, autoStart=True):
        # params
        self.manager = manager
        self.host = host
        self.port = port
        self.threaded = threaded

        # attrs
        self._kill = False
        self.oscServer = None
        self.thread = None

        if autoStart:
            self.start()

    def setup(self):
        if self.oscServer != None:
            self.destroy()

        ColorTerminal().output("Starting OSC server with host {0} and port {1}".format(self.host, self.port))
        self.oscServer = OSCServer((self.host, self.port))
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
        if self.manager:
            self.manager.processRigidBodyJson(data[0])

    def handleTimeout(self):
        if self.oscServer != None:
            self.oscServer.timed_out = True

    def start(self):
        if not self.threaded:
            self.setup()
            return

        if self.thread and self.thread.isAlive():
            ColorTerminal().warn("OscReader - Can't start while a thread is already running")
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

    def threaded_loop(self):
        self.setup()

        while not self._kill:
            self.update()

        self.destroy()
