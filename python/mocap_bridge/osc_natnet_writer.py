try:
    import OSC
except ImportError:
    print bcolors.FAIL + "Error importing library, please install pyOSC by running: sudo pip install pyOSC"+ bcolors.ENDC
from natnet_writer import NatNetWriter

class OSCNatNetWriter(NatNetWriter):
    def __init__(self, host="127.0.0.1", port=8080, autoConnect=True):
        super(OSCNatNetWriter, self).__init__()
        self.host = host
        self.port = port
        self.isConnected = False
        self.autoConnect = True
        self.client = OSC.OSCClient()

    def openStream(self):
        self.client.connect((self.host, int(self.port)))
        self.isConnected = True

    def closeStream(self):
        self.client.close()
        self.isConnected = False

    def writeDataFrame(self, reader, timestamp):
        allrb = reader.getAllRigidbodies()
        #import pdb; pdb.set_trace()
        for id in allrb.keys():
            self.sendRigidbody(allrb[id])

    def sendRigidbody(self, rb):
        json = rb.toJSON()
        self._sendMessage("/rigidbody", json)

    def _sendMessage(self, tag, content):
        msg = OSC.OSCMessage()
        msg.setAddress(tag) # set OSC address
        msg.append(content)
        try:
            self.client.send(msg)
        except:
            self.openStream()
