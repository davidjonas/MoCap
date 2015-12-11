import sys
from natnet_parser import NatNetParser
import json
from datetime import datetime

class JSONPlayer:
	def __init__(self, path=None, natnet=None):
		# params
		self.path = path
		self.natnet = natnet

		# attributes
		self.file = None

		if self.natnet == None:
			natnet = NatNetParser() # we'll just create our own, no need to connect anyway

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

	def _playFrame(self, data):
		print("TODO: play: "+data)



if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("Please specify a source file")
		exit(1)
	
	filePath = sys.argv[1]		

	player = JSONPlayer(path=filePath)
	player.start()
