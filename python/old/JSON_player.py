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
	def __init__(self, path=None, natnet=None, loop=True):
		# params
		self.path = path
		self.natnet = natnet
		self.loop = loop

		# attributes
		self.file = None
		self.startTime = None

		if self.natnet == None:
			self.natnet = NatNetParser() # we'll just create our own, no need to connect anyway

	def start(self):
		playcount = 0
		while playcount == 0 or self.loop == True:
			self.file = open(self.path, 'r')
			self.startTime = datetime.now()
			self._play()
			self.stop()

	def _play(self):
		while True:
			# get next frame data
			data = self._nextFrameData()

			# if none, we've probably reached the end of the file, time to stop
			if data == None:
				
				return

			# wait until it is time to play the frame
			while ((datetime.now() - self.startTime).total_seconds() < data['t']):
				pass

			# 'play' the data
			self._playFrame(data)

	def _nextFrameData(self):
		while True:
			# read next line from the file
			line = self.file.readline()

			# return None when end-of-file is reached
			if line == '':
				return None

			# try to parse json
			try:
				data = json.loads(line)
				return data
			except (ValueError):
				pass

	def stop(self):
		if self.file:
			self.file.close()
			self.file = None

	def _playFrame(self, data):
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
		print("Please specify a source file as first argument")
		exit(1)
	
	filePath = sys.argv[1]		
	player = JSONPlayer(path=filePath)

	osc = OSCLink("127.0.0.1", 8080)
	player.natnet.updated += updateOSC

	player.start()
