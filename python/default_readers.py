from terminal_colors import bcolors

try:
    import optirx as rx
except ImportError:
    print bcolors.FAIL + "Error importing library, please install optirx by running: sudo pip install optirx"+ bcolors.ENDC
from natnet_reader import NatNetReader
from event import Event
from natnet_data import *
import json

class LiveNatnetReader(NatNetReader):
    def __init__(self, host, multicast, port):
        super(LiveNatNetReader, self).__init__()
        self.host = host
        self.multicast = multicast
        self.port = port
        self.version = (2, 7, 0, 0)
        self.connected = False
        self.dsock = None
        self.connectionLost = Event()


    def openStream(self):
        print(bcolors.OKBLUE + "Connecting to %s : %s" % (self.host, self.port) + bcolors.ENDC)
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
            self.connectionLost()

        return self.connected

    def closeStream(self):
        self.dsock = None
        self.connected = False
        self.connectionLost()

    def readDataFrame(self):
        data = self.dsock.recv(rx.MAX_PACKETSIZE)
        packet = rx.unpack(data, version=self.version)
        if type(packet) is rx.SenderData:
            setVersion(packet.natnet_version)
        self.parse(packet)

    def parse(self, packet):
        for s in packet.skeletons:
            skel = self.getOrCreateSkeleton(s.id)
            for r in s.rigid_bodies:
                rb = RigidBody(obj=r)
                skel.addOrUpdateRigidbody(rb)

        for r in packet.rigid_bodies:
            rb = RigidBody(obj=r)
            self.addOrUpdateRigidbody(rb)

class JSONNatNetReader(NatNetReader):
    def __init__(self, path, loop=True, sync=False):
        super(JSONNatNetReader, self).__init__()
        # params
        self.path = path
        self.loop = loop
        self.sync = sync

        # attributes
        self.file = None
        # isPlaying = False

    def setLoop(self, loop):
        self.loop = loop

    def openStream(self):
        print "opening file %s." % self.path
        self.file = open(self.path, 'r')

    def closeStream(self):
        self.file.close()
        self.file = None

    def readDataFrame(self):
        data = self._nextJsonLine()

        if data == None:
            return

        try:
            # are we performing frame time-syncs?
            if self.sync:
                # wait until it's time for the next
                dt = self.getTime()
                while data["t"] > dt:
                    pass

            for rigid in data['rigidbodies']:
                rb = RigidBody(id=rigid["id"], position=rigid["p"], orientation=rigid["r"])
                self.addOrUpdateRigidbody(rb)
        except:
            print(bcolors.FAIL +"Error parsing file."+ bcolors.ENDC)

    def _nextJsonLine(self):
        if self.file == None:
            return None

        # this limit avoid we're getting stuck in an endless loop if
        # there are no valid json lines in the file and looping is enabled
        maxTries = 10
        tryCount = 0

        while tryCount < maxTries:
            line = self._readLine()

            try:
                # parse json string
                data = json.loads(line)
                # return parsed string as json object
                return data
            except ValueError:
                # probably a comment line
                # we'll just ignore any non-json line in the file
                pass

            # next try
            tryCount += 1

    def _readLine(self):
        # we need a file handle
        if self.file is None:
            #print "File does not exist."
            return None

        # grab next line from file the file
        line = self.file.readline()

        # if we've got something, return it
        if line != '':
            return line

        # got nothing, probably reached the end of the file
        # if we're looping, start back at the beginning of the file and try again
        if self.loop:
            self.file.seek(0)
            return self._readLine()

        # nothing (more) to read and we're not looping
        self.closeStream()
        return None
