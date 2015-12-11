import Tkinter
from natnet_parser import NatNetParser
from OSC_link import OSCLink

def update():
    global natnet
    for rb in natnet.rigidbodies:
        osc.sendRigibodyAsJSON(rb)

if __name__ == "__main__":
	natnet = NatNetParser(host="0.0.0.0", port="1511")
	# osc = OSCLink("127.0.0.1", 8080)
	osc = OSCLink("145.107.192.137", 8080)

	natnet.updated += update
	natnet.connect()
	natnet.run()