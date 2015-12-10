
from terminal_colors import bcolors

try:
    import optirx as rx
except ImportError:
    print bcolors.FAIL + "Error importing library, please install optirx by running: sudo pip install optirx"+ bcolors.ENDC
from event import Event
import threading


class NatNetParser(threading.Thread):
    """
    NatNetParser class connects to a NatNet server, reads MoCap data,
    parses it and makes it available as python objects.
    """

    def __init__(self, host=None, multicast=None, port=None):
        threading.Thread.__init__(self)
        self.host = host
        self.multicast = multicast
        self.port = int(port)
        self.skeletons = []
        self.rigidbodies = []
        self.version = (2, 7, 0, 0)
        self.updated = Event()
        self.connectionLost = Event()
        self.connected = False

    def setVersion(self, version):
        self.version=version

    def getVersion(self):
        return version

    def connect(self):
        print(bcolors.OKBLUE + "Connecting to %s : %s" % (self.host, self.port) + bcolors.ENDC)
        try:
            if self.host is None:
                self.dsock = rx.mkdatasock() #Connecting to localhost
            elif self.multicast is not None and self.port is not None:
                self.dsock = rx.mkdatasock(ip_address=self.host, multicast_address=self.multicast, port=self.port) #Connecting to multicast address
            else:
                self.dsock = rx.mkdatasock(ip_address=self.host, port=self.port) # Connecting to IP address
            self.connected = True
        except:
            self.connected = False
            print(bcolors.FAIL +"There was an error connecting"+ bcolors.ENDC)
            raise

        return self.connected

    def disconnect():
        self.dsock = None
        self.connected = False
        self.connectionLost()

    def isConnected(self):
        return self.connected

    def countSkeletons(self):
        return len(self.skeletons)

    def countRigidbodies(self):
        return len(self.rigidbodies)

    def getSkeleton(self, index):
        if index > -1 and index < self.countSkeletons():
            return skeletons[index]
        else:
            return None

    def getRigidbody(self, index):
        if index > -1 and index < self.countRigidbodies():
            return self.rigidbodies[index]
        else:
            return None

    def run(self):
        while True:
            try:
                data = self.dsock.recv(rx.MAX_PACKETSIZE)
                packet = rx.unpack(data, version=self.version)
                if type(packet) is rx.SenderData:
                    setVersion(packet.natnet_version)
                self.parse(packet)
                self.updated()
            except:
                print bcolors.FAIL + "Disconnected from server." + bcolors.ENDC
                raise
                self.disconnect()
                break;

    def parse(self, packet):
        #import pdb; pdb.set_trace()
        self.skeletons = packet.skeletons
        self.rigidbodies = []

        for s in packet.skeletons:
            for r in s.rigid_bodies:
                self.rigidbodies.append(r)
