import Tkinter
from natnet_parser import NatNetParser
from OSC_link import OSCLink

natnet = NatNetParser(host="0.0.0.0", port="1511")
osc = OSCLink("127.0.0.1", 8080)

def update():
    global natnet
    for rb in natnet.rigidbodies:
        osc.sendRigibodyAsJSON(rb)

natnet.updated += update
natnet.connect()
natnet.run()
