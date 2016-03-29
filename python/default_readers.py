from terminal_colors import bcolors

try:
    import optirx as rx
except ImportError:
    print bcolors.FAIL + "Error importing library, please install optirx by running: sudo pip install optirx"+ bcolors.ENDC
from natnet_reader import NatNetReader
from event import Event
from natnet_data import *
import json
import time
from datetime import datetime

class LiveNatnetReader(NatNetReader):
    def __init__(self, host, multicast, port):
        super(LiveNatnetReader, self).__init__()
        self.host = host
        self.multicast = multicast
        self.port = port
        self.version = (2, 7, 0, 0)
        self.connected = False
        self.dsock = None
        self.connectionLost = Event()
        self.max_delay_in_seconds = 0.2
        self.firstTimestamp = 0


    def openStream(self):
        print(bcolors.OKGREEN + "Connecting to NatNet @ %s : %s" % (self.host, self.port) + bcolors.ENDC)
        try:
            if self.host is None:
                self.dsock = rx.mkdatasock() #Connecting to localhost
            elif self.multicast is not None and self.port is not None:
                self.dsock = rx.mkdatasock(ip_address=self.host, multicast_address=self.multicast, port=int(self.port)) #Connecting to multicast address
            else:
                self.dsock = rx.mkdatasock(ip_address=self.host, port=int(self.port)) # Connecting to IP address
            self.connected = True
        except:
            self.connected = False
            print(bcolors.FAIL +"There was an error connecting"+ bcolors.ENDC)
            raise
            self.connectionLost()

        return self.connected

    def closeStream(self):
        print(bcolors.OKBLUE + "Disconnected from NatNet" + bcolors.ENDC)
        if self.dsock is not None:
            self.dsock.close()
        self.dsock = None
        self.connected = False
        self.connectionLost()

    def readDataFrame(self):
        data = self.dsock.recv(rx.MAX_PACKETSIZE)
        packet = rx.unpack(data, version=self.version)

        if self.firstTimestamp == 0 or self.firstTimestamp > packet.timestamp:
            self.firstTimestamp = packet.timestamp
            self.startTime = datetime.now()

        if packet.timestamp - self.firstTimestamp < datetime.now() - self.startTime + self.max_delay_in_seconds:
            if type(packet) is rx.SenderData:
                setVersion(packet.natnet_version)
            self.parse(packet)

    def parse(self, packet):
        #for s in packet.skeletons:
            #skel = self.getOrCreateSkeleton(s.id)
            #for r in s.rigid_bodies:
                #self.updateRigidbody(obj)
                #rb = RigidBody(obj=r)
                #skel.addOrUpdateRigidbody(rb)

        for r in packet.rigid_bodies:
            self.updateRigidbody(obj)
            #rb = RigidBody(obj=r)
            #self.addOrUpdateRigidbody(rb)

class JSONNatNetReader(NatNetReader):
    def __init__(self, path, loop=True):
        super(JSONNatNetReader, self).__init__()
        self.path = path
        self.loop = loop
        self.file = None
        isPlaying = False

    def setLoop(self, loop):
        self.loop = loop

    def openStream(self):
        print "opening file %s." % self.path
        self.file = open(self.path, 'r')

    def closeStream(self):
        self.file.close()

    def readDataFrame(self):
        if self.file is not None:
            line = self.file.readline()
            if line == '':
                if self.loop:
                    self.file.seek(0)
                    line = self.file.readline()
                    self.startTime = datetime.now()
                else:
                    self.closeStream()
            try:
                data = json.loads(line)
                dt = self.getTime()
                if data["t"] > dt:
                    for rigid in data['rigidbodies']:
                        #rb = RigidBody(id=rigid["id"], position=rigid["p"], orientation=rigid["r"])
                        #self.addOrUpdateRigidbody(rb)
                        obj = {
                            "id":rigid["id"],
                            "position":rigid["p"],
                            "orientation":rigid["r"]
                        }
                        self.updateRigidbody(obj)
            except:
                print(bcolors.FAIL +"Error parsing file."+ bcolors.ENDC)
                raise
        else:
            #print "File does not exist."
            pass
