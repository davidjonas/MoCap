from mocap_bridge.utils.color_terminal import ColorTerminal

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server

import threading

class OscReader:
    def __init__(self, host="127.0.0.1", port=8080, manager=None, threaded=False, autoStart=True):
        # params
        self.manager = manager
        self.host = host
        self.port = port
        self.threaded = threaded

        # attrs
        self.started = False
        self._kill = False
        self.oscServer = None
        self.thread = None

        if autoStart:
            self.start()

    def __del__(self):
        # ColorTerminal().warn('OscReader-__del__')
        # make sure the OSC connection socket gets freed up
        self.stop()

    def setup(self):
        # ColorTerminal().warn('OscReader-setup')
        if self.oscServer != None:
            self.destroy()

        ColorTerminal().output("Starting OSC Server with host {0} and port {1}".format(self.host, self.port))
        dispatcher = Dispatcher()
        dispatcher.map("/rigidbody", self.oscRigidBodyHandler)

        try:
            self.oscServer = osc_server.BlockingOSCUDPServer((self.host, self.port), dispatcher)
            self.oscServer.handle_timeout = self.handleTimeout
            self.oscServer.timeout=0
            #self.oscServer.serve_forever()

        except OSError as err:
            ColorTerminal().fail("Could not create OSC server: ", err)
            self.oscServer = None

        ColorTerminal().success("OSC Server running")

    def destroy(self):
        # ColorTerminal().warn('OscReader-destroy')
        if self.oscServer == None:
            return

        self.oscServer.server_close()
        ColorTerminal().success("OSC Server closed")
        self.oscServer = None

    def update(self):
        # ColorTerminal().warn('OscReader-update')

        if self.oscServer == None or not self.started:
            return

        # we'll enforce a limit to the number of osc requests
        # we'll handle in a single iteration, otherwise we might
        # get stuck in processing an endless stream of data
        limit = 10
        count = 0

        # # clear timed_out flag
        self.oscServer.timed_out = False

        # # handle all pending requests then return
        while not self.oscServer.timed_out and count < limit:
            self.oscServer.handle_request()
            count += 1

    def oscRigidBodyHandler(self, addr=None, data=None, tags=None, client_address=None):
        # print('OscReader.oscRigidBodyHandler', addr, data)
        # readers can interface with the mocap data manager directly (most efficient)
        if self.manager and data:
            self.manager.processRigidBodyJson(data)

    def handleTimeout(self):
        if self.oscServer != None:
            self.oscServer.timed_out = True

    def start(self):
        ColorTerminal().warn('OscReader-start')
        if not self.threaded:
            self.setup()
            self.started = True
            return

        if self.thread and self.thread.isAlive():
            ColorTerminal().warn("OscReader - Can't start while a thread is already running")
            return

        self._kill = False
        # threaded loop method will call setup
        self.thread = threading.Thread(target=self.threaded_loop)
        self.thread.start()

    def stop(self):
        # ColorTerminal().warn('OscReader-stop')
        if self.threaded:
            # threaded loop method will call destroy
            self._kill = True
        else:
            self.destroy()
            self.started = False

    def threaded_loop(self):
        ColorTerminal().warn('OscReader-threaded_loop')
        self.started = True
        self.setup()

        while not self._kill:
            self.update()

        self.destroy()
        self.started = False
