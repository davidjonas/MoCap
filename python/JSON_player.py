import sys
from natnet_parser import NatNetParser
import json
from datetime import datetime
from OSC_link import OSCLink

# dummy class to represent parsed json rigidbody objects,
# TODO: figure out which class the natnet parser uses
class RigidBodyClass:
	pass

class JSONPlayer:
	def __init__(self, path=None, natnet=None):
		# params
		self.path = path
		self.natnet = natnet

		# attributes
		self.file = None

		if self.natnet == None:
			self.natnet = NatNetParser() # we'll just create our own, no need to connect anyway

	def start(self):
		self.file = open(self.path, 'r')

		while True:
			line = self.file.readline()
			if line == '':
				break;

			self._playFrame(line)

		self.stop()

	def stop(self):
		if self.file:
			self.file.close()
			self.file = None

	def _playFrame(self, data_text):
		#print("TODO: play: "+data)
		try:
			data = json.loads(data_text)
		except (ValueError):
			return # invalid line, could be a comment

		self.natnet.rigidbodies = []

		for b in data['rigidbodies']:
			rb = RigidBodyClass() # TODO: figure out what class the original natnet parses uses/gets
			rb.id = b['id']
			rb.position = b['p']
			rb.orientation = b['r']
			self.natnet.rigidbodies.append(rb)

		self.natnet.updated()


def updateOSC():
    global player
    global osc
    for rb in player.natnet.rigidbodies:
        osc.sendRigibodyAsJSON(rb)


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Please specify a source file")
		exit(1)
	
	filePath = sys.argv[1]		
	player = JSONPlayer(path=filePath)

	osc = OSCLink("145.107.192.137", 8080)
	player.natnet.updated += updateOSC

	player.start()
