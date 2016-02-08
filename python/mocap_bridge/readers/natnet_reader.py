from mocap_bridge.utils.color_terminal import ColorTerminal
from mocap_bridge.utils.event import Event

try:
    import optirx as rx
except ImportError:
    ColorTerminal().fail("Error importing library, please install optirx by running: sudo pip install optirx")

import threading

class NatnetReader:
    def __init__(self, host='0.0.0.0', multicast=None, port=1511, manager=None, threaded=False, autoStart=True):
        self.host = host
        self.multicast = multicast
        self.port = port
        self.manager = manager
        self.threaded = threaded

        self.version = (2, 7, 0, 0)
        self.connected = False
        self.dsock = None
        self.connectionLostEvent = Event()

        self.thread = None
        self._kill = False

        if autoStart:
            self.start()

    def setup(self):
        self._connect()

    def destroy(self):
        self._disconnect()

    def update(self):
        # print('NatnetReader.update')
        data = self.dsock.recv(rx.MAX_PACKETSIZE)
        packet = rx.unpack(data, version=self.version)

        if type(packet) is rx.SenderData:
            setVersion(packet.natnet_version)
        self._parse(packet)

    def start(self):
        if not self.threaded:
            self.setup()
            return

        if self.thread and self.thread.isAlive():
            ColorTerminal().warn("OscReader - Can't start while a thread is already running")
            return

        self._kill = False

        # threaded loop method will call setup
        self.thread = threading.Thread(target=self._threaded_main)
        self.thread.start()

    def stop(self):
        if self.threaded:
            # threaded loop method will call destroy
            self._kill = True
        else:
            self.destroy()

    def _threaded_main(self):
        self.setup()

        while not self._kill:
            self.update()

        self.destroy()

    def _connect(self):
        ColorTerminal().blue("Connecting to %s : %s" % (self.host, self.port))

        try:
            if self.host is None:
                self.dsock = rx.mkdatasock() #Connecting to localhost
            elif self.multicast is not None and self.port is not None:
                self.dsock = rx.mkdatasock(ip_address=self.host, multicast_address=self.multicast, port=int(self.port)) #Connecting to multicast address
            else:
                self.dsock = rx.mkdatasock(ip_address=self.host, port=int(self.port)) # Connecting to IP address
            self.connected = True
            ColorTerminal().green("Connected")
        except:
            print(bcolors.FAIL +"There was an error connecting"+ bcolors.ENDC)
            self.disconnect()

        return self.connected

    def _disconnect(self):
        self.dsock = None
        self.connected = False
        self.connectionLostEvent()

    def _parse(self, packet):
        if not self.manager:
            return
        # print('_parse:',packet)
        for skeletonObj in packet.skeletons:
            skeleton = self.manager.getOrCreateSkeleton(skeletonObj.id)
            for rbObj in skeletonObj.rigid_bodies:
                rb = RigidBody(obj=rbObj)
                skeleton.addOrUpdateRigidbody(rb)

        for rbObj in packet.rigid_bodies:
            # print('rb', rbObj)
            self.manager.processRigidBodyObject(rbObj)
