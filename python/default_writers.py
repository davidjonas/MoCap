try:
    import OSC
except ImportError:
    print bcolors.FAIL + "Error importing library, please install pyOSC by running: sudo pip install pyOSC"+ bcolors.ENDC
from natnet_writer import NatNetWriter
from terminal_colors import bcolors
import json

class OSCNatNetWriter(NatNetWriter):
    def __init__(self, host="127.0.0.1", port="8080", autoConnect=True):
        super(OSCNatNetWriter, self).__init__()
        self.host = host
        self.port = port
        self.connected = False
        self.autoConnect = True
        print(bcolors.OKGREEN + "Starting OSC client at %s:%s" % (host, port) + bcolors.ENDC)
        self.client = OSC.OSCClient()

    def openStream(self):
        self.client.connect((self.host, int(self.port)))
        self.connected = True
        #print(bcolors.OKGREEN + "OSC client connected" + bcolors.ENDC)

    def closeStream(self):
        print(bcolors.OKBLUE + "Stopping OSC client" + bcolors.ENDC)
        self.client.close()
        self.connected = False

    def writeDataFrame(self, reader, timestamp):
        allrb = reader.rigidbodies
        for id in allrb.keys():
            self.writeRigidbody(allrb[id])

        #for s in reader.skeletons:
            #self.writeSkeleton(reader.skeletons[s])

    def writeRigidbody(self, rb):
        j = json.dumps(rb)
        self._sendMessage("/rigidbody", j)

    def writeSkeleton(self, sk):
        j = sk.toJSON()
        self._sendMessage("/skeleton", j)

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
