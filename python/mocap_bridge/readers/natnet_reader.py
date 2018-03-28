from mocap_bridge.utils.color_terminal import ColorTerminal
from mocap_bridge.utils.event import Event

try:
    import optirx as rx
except ImportError:
    ColorTerminal().fail("Error importing library, please install optirx by running: sudo pip install optirx")

import threading

class NatnetReader:
    def __init__(self, host='0.0.0.0', multicast=None, port=1511, manager=None, threaded=False, readMarkers=False, ingestSkeletonRigidBodies=False, autoStart=True):
        self.host = host
        self.multicast = multicast
        self.port = port
        self.manager = manager
        self.threaded = threaded
        self.readMarkers = readMarkers
        self.ingestSkeletonRigidBodies = ingestSkeletonRigidBodies

        self.version = (2, 9, 0, 0)
        self.connected = False
        self.dsock = None
        self.connection_status = None

        self.connectionLostEvent = Event()
        self.connectEvent = Event()
        self.connectionStatusUpdateEvent = Event()

        self.thread = None
        self._kill = False

        if autoStart:
            self.start()

    def setup(self):
        self._connect()

    def destroy(self):
        self._disconnect()

    def update(self):
        if not self.dsock:
            return

        # print('NatnetReader.update')
        data = None

        try:
            data = self.dsock.recv(rx.MAX_PACKETSIZE)

            if self.connection_status != None:
                self.connection_status = None
                self.connectionStatusUpdateEvent(self)
        except Exception as e:
            # error: [Errno 35] Resource temporarily unavailable
            # print('socket receive err: ', e.strerror)
            if self.connection_status != e.strerror:
                self.connection_status = e.strerror
                self.connectionStatusUpdateEvent(self)

        if data:
            packet = rx.unpack(data, version=self.version)
            if type(packet) is rx.SenderData:
                self.setVersion(packet.natnet_version)
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

    def configure(self, host=None, multicast=None, port=None):
        if host: self.host = host
        if multicast: self.multicast = multicast
        if port: self.port = port

        # if connection is active; reconnect with new configuration
        if (host or port or multicast) and self.connected:
            self.stop()
            self.start()

    def setVersion(self, version):
        self.version=version

    def _threaded_main(self):
        self.setup()

        while not self._kill:
            self.update()

        self.destroy()

    def _connect(self):


        try:
            if self.host is None:
                self.dsock = rx.mkdatasock() #Connecting to localhost
            elif self.multicast is not None and self.multicast is not '' and self.port is not None:
                ColorTerminal().blue("Connecting to natnet on %s@%s (multicast: %s)" % (self.host, self.port, self.multicast))
                self.dsock = rx.mkdatasock(ip_address=self.host, multicast_address=self.multicast, port=int(self.port)) #Connecting to multicast address
            else:
                ColorTerminal().blue("Connecting to natnet on %s@%s" % (self.host, self.port))
                self.dsock = rx.mkdatasock(ip_address=self.host, port=int(self.port)) # Connecting to IP address

            self.dsock.setblocking(0)
            self.connected = True
            self.connectEvent(self)
            ColorTerminal().green("Connected")
        except:
            ColorTerminal().red("There was an error connecting")
            self._disconnect()


        return self.connected

    def _disconnect(self):
        self.dsock = None
        self.connected = False
        self.connectionLostEvent(self)
        ColorTerminal().green("Disconnected")

    def _parse(self, packet):
        if not self.manager:
            return

        # print('_parse:',packet)
        # print('parse dir:', dir(packet))
        if self.readMarkers and 'other_markers' in dir(packet):
            self.manager.processMarkersData(packet.other_markers, 'NatnetReader')

        self._ingestRigidBodyData(packet.rigid_bodies, 'NatnetReader')
        self._ingestSkeletonData(packet.skeletons, 'NatnetReader')
        self.manager.finishBatch('NatnetReader')

    def _ingestSkeletonData(self, skData, batch=None):
        # print('_ingestSkeletonData: ', skData)

        for skeletonObj in skData:
            # get rigid body IDs for current skeleton
            rigidBodyIds = map(lambda rb: rb.id, skeletonObj.rigid_bodies)
            # ingest (create or update) skeleton
            self.manager.processSkeletonObject({'id': skeletonObj.id, 'rigid_body_ids': rigidBodyIds, 'rigid_bodies': skeletonObj.rigid_bodies})
            # ingest skeleton's rigid bodies, only when enabled (might contain the same rigid bodies as packet's root level)
            if hasattr(skeletonObj, 'rigid_bodies') and self.ingestSkeletonRigidBodies:
                self._ingestRigidBodyData(skeletonObj.rigid_bodies, batch)

    def _ingestRigidBodyData(self, rbData, batch=None):
        # print('_ingestRigidBodyData: ', rbData)
        for rbObj in rbData:
            # ingest (create or update) rigid body
            # print('_ingestRigidBodyData, single rb: ', rbObj)
            self.manager.processRigidBodyObject(rbObj, batch)
