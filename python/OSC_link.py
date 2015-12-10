from terminal_colors import bcolors
import sys
import json
try:
    import OSC
except ImportError:
    print bcolors.FAIL + "Error importing library, please install pyOSC by running: sudo pip install pyOSC"+ bcolors.ENDC
from event import Event



class OSCLink(object):
    """
    OSC link to send translated MoCap data from NatNet
    """

    def __init__(self, host, port):
        self.isConnected = False
        self.c = OSC.OSCClient()
        self.send_address = (host, int(port))
        self._connect()

    def _connect(self):
        self.c.connect(self.send_address)
        self.isConnected = True

    def close(self):
        self.c.close()

    def _sendMessage(self, tag, content):
        msg = OSC.OSCMessage()
        msg.setAddress(tag) # set OSC address
        msg.append(content)
        #TODO: This is debug code
        #print bcolors.OKGREEN + "Sending message:" + bcolors.ENDC
        #print msg
        self.c.send(msg)

    def sendRigibodyAsJSON(self, rigidbody):
        r = {
            'id':rigidbody.id,
            'position':rigidbody.position,
            'orientation':rigidbody.orientation,
        }
        j = json.dumps(r)
        self._sendMessage("/rigidbody", j)

    def sendRigidBody(self, rigidbody, prefix=None):
        #position
        self._sendMessage("/rb_%s_positionX"%prefix is not None and prefix or rigidbody.id, rigidbody.position[0])
        self._sendMessage("/rb_%s_positionY"%prefix is not None and prefix or rigidbody.id, rigidbody.position[1])
        self._sendMessage("/rb_%s_positionZ"%prefix is not None and prefix or rigidbody.id, rigidbody.position[2])

        #orientation
        self._sendMessage("/rb_%s_orientationX"%prefix is not None and prefix or rigidbody.id, rigidbody.position[0])
        self._sendMessage("/rb_%s_orientationY"%prefix is not None and prefix or rigidbody.id, rigidbody.position[1])
        self._sendMessage("/rb_%s_orientationZ"%prefix is not None and prefix or rigidbody.id, rigidbody.position[2])
        self._sendMessage("/rb_%s_orientationW"%prefix is not None and prefix or rigidbody.id, rigidbody.position[3])
