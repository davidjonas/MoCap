# import Tkinter
from natnet_parser import NatNetParser
from JSON_link import JSONLink

if __name__ == "__main__":
	natnet = NatNetParser(host="0.0.0.0", port="1511")
	json_recorder = JSONLink(natnet=natnet, autoStart=True) #OSCLink(file="recording")
	natnet.connect()
	natnet.run()
