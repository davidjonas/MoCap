##First test, this file is here for historical reasons, this was the first test in the mocap lab. It is working though.

#Fancy console color
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

import sys
import json
import OSC

# =====OSC Connection=====
host = "localhost"
send_address = '10.200.200.35', 8000

# OSC basic client
c = OSC.OSCClient()
c.connect( send_address ) # set the address for all following messages

print bcolors.OKGREEN + "communications established." + bcolors.ENDC
print bcolors.OKGREEN + "Enjoy..." + bcolors.ENDC


def sendBone(rigidbody):
    r = {
        'id':rigidbody.id,
        'position':rigidbody.position,
        'orientation':rigidbody.orientation,
    }
    j = json.dumps(r)
    msg = OSC.OSCMessage()
    msg.setAddress("/bone") # set OSC address
    msg.append(j)
    c.send(msg)

# =========

try:
    import optirx as rx
    print bcolors.OKGREEN + "Libraries imported correctly" + bcolors.ENDC
except ImportException:
    print bcolors.FAIL + "Error importing library, please install optirx by running: sudo pip install optirx"+ bcolors.ENDC


if len(sys.argv) == 4:
    print bcolors.OKGREEN + "connecting to IP address %s / multicast address %s with port %s" % (sys.argv[1], sys.argv[2], sys.argv[3]) + bcolors.ENDC
    dsock = rx.mkdatasock(ip_address=sys.argv[1], multicast_address=sys.argv[2], port=int(sys.argv[3]))
elif len(sys.argv) == 3:
    print bcolors.OKGREEN + "connecting to IP address %s with port %s" % (sys.argv[1], sys.argv[2]) + bcolors.ENDC
    dsock = rx.mkdatasock(ip_address=sys.argv[1], port=int(sys.argv[2]))
else:
    print bcolors.OKGREEN + "connecting to localhost" + bcolors.ENDC
    dsock = rx.mkdatasock()

version = (2, 7, 0, 0)  # NatNet version to use

while True:
    data = dsock.recv(rx.MAX_PACKETSIZE)
    packet = rx.unpack(data, version=version)
    if type(packet) is rx.SenderData:
        version = packet.natnet_version
    for r in packet.skeletons[0].rigid_bodies:
        sendBone(r)
