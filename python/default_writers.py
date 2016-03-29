try:
    import OSC
except ImportError:
    print bcolors.FAIL + "Error importing library, please install pyOSC by running: sudo pip install pyOSC"+ bcolors.ENDC
from natnet_writer import NatNetWriter
from terminal_colors import bcolors

class OSCNatNetWriter(NatNetWriter):
    def __init__(self, host="127.0.0.1", port="8080", autoConnect=True):
        super(OSCNatNetWriter, self).__init__()
        self.host = host
        self.port = port
        self.isConnected = False
        self.autoConnect = True
        print(bcolors.OKBLUE + "Starting OSC client at %s:%s" % (host, port) + bcolors.ENDC)
        self.client = OSC.OSCClient()

    def openStream(self):
        self.client.connect((self.host, int(self.port)))
        self.isConnected = True
        #print(bcolors.OKGREEN + "OSC client connected" + bcolors.ENDC)

    def closeStream(self):
        self.client.close()
        self.isConnected = False

    def writeDataFrame(self, reader, timestamp):
        allrb = reader.rigidbodies
        for id in allrb.keys():
            self.writeRigidbody(allrb[id])

        for s in reader.skeletons:
            self.writeSkeleton(reader.skeletons[s])

    def writeRigidbody(self, rb):
        json = rb.toJSON()
        self._sendMessage("/rigidbody", json)

    def writeSkeleton(self, sk):
        json = sk.toJSON()
        self._sendMessage("/skeleton", json)

        for rb in sk.rigidbodies:
                self.sendRigidbody(sk.rigidbodies[rb])

    def _sendMessage(self, tag, content):
        msg = OSC.OSCMessage()
        msg.setAddress(tag) # set OSC address
        msg.append(content)
        try:
            self.client.send(msg)
        except:
            self.openStream()
