from terminal_colors import bcolors
from mocap_interface.rigid_body import RigidBody # , Skeleton # Sekeleton is not yet supported
from natnet_reader import NatNetReader

import json

class JSONNatNetReader(NatNetReader):
    def __init__(self, path, loop=True, sync=False):
        super(JSONNatNetReader, self).__init__()
        # params
        self.path = path
        self.loop = loop
        self.sync = sync

        # attributes
        self.file = None
        # isPlaying = False

    def setLoop(self, loop):
        self.loop = loop

    def openStream(self):
        print "opening file %s." % self.path
        self.file = open(self.path, 'r')

    def closeStream(self):
        self.file.close()
        self.file = None

    def readDataFrame(self):
        data = self._nextJsonLine()

        if data == None:
            return

        try:
            # are we performing frame time-syncs?
            if self.sync:
                # wait until it's time for the next
                dt = self.getTime()
                while data["t"] > dt:
                    pass

            for rigid in data['rigidbodies']:
                rb = RigidBody(id=rigid["id"], position=rigid["p"], orientation=rigid["r"])
                self.addOrUpdateRigidbody(rb)
        except:
            print(bcolors.FAIL +"Error parsing file."+ bcolors.ENDC)

    def _nextJsonLine(self):
        if self.file == None:
            return None

        # this limit avoid we're getting stuck in an endless loop if
        # there are no valid json lines in the file and looping is enabled
        maxTries = 10
        tryCount = 0

        while tryCount < maxTries:
            line = self._readLine()

            try:
                # parse json string
                data = json.loads(line)
                # return parsed string as json object
                return data
            except ValueError:
                # probably a comment line
                # we'll just ignore any non-json line in the file
                pass

            # next try
            tryCount += 1

    def _readLine(self):
        # we need a file handle
        if self.file is None:
            #print "File does not exist."
            return None

        # grab next line from file the file
        line = self.file.readline()

        # if we've got something, return it
        if line != '':
            return line

        # got nothing, probably reached the end of the file
        # if we're looping, start back at the beginning of the file and try again
        if self.loop:
            self.file.seek(0)
            return self._readLine()

        # nothing (more) to read and we're not looping
        self.closeStream()
        return None
