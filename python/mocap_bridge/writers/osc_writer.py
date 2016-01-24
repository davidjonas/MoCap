from mocap_bridge.utils.color_terminal import ColorTerminal

try:
    import OSC
except ImportError:
    ColorTerminal().fail("Error importing library, please install pyOSC by running: sudo pip install pyOSC")

class OscWriter:
    def __init__(self, host="127.0.0.1", port=8080, manager=None, autoStart=True):
        self.host = host
        self.port = port

        self.client = OSC.OSCClient()
        self.running = False

        self.manager = manager

        if autoStart == True:
            self.start()

    def connect(self):
        self.client.connect((self.host, int(self.port)))
        ColorTerminal().success("OSC client connected")

    def disconnect(self):
        self.client.close()
        ColorTerminal().success("OSC client closed")

    def start(self):
        self.connect()

        if self.manager != None:
            # the event class already discards duplicates, so no need to check
            self.manager.updateEvent += self.onUpdate

        self.running = True

    def stop(self):
        self.disconnect()
        self.running = False

    def onUpdate(self, manager):
        if not self.running:
            return

        for rigid_body in self.manager.allRigidBodies():
            self._sendMessage("/rigidbody", rigid_body.toJSON())

    def _sendMessage(self, tag, content):
        msg = OSC.OSCMessage()
        msg.setAddress(tag) # set OSC address
        msg.append(content)

        try:
            self.client.send(msg)
        except OSC.OSCClientError as err:
            ColorTerminal().warn("OSC failure: {0}".format(err))
            self.connect()
