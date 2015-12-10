import Tkinter
from natnet_parser import NatNetParser
#from OSC_link import OSCLink

natnet = NatNetParser(host="0.0.0.0", port="1511")

def update():
    global natnet
    rb = natnet.getRigidbody(0)
    print(rb.position[0])

natnet.updated += update
natnet.connect()
natnet.run()
