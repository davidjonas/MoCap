from mocap_bridge.utils.color_terminal import ColorTerminal

import json
import threading
from datetime import datetime

class JsonReader:
    def __init__(self, path, loop=True, sync=False, threaded=False, manager=None, autoStart=True):
        # params
        self.path = path
        self.loop = loop
        self.sync = sync
        self.threaded = threaded
        self.manager = manager

        # attributes
        self.file = None
        self.thread = None
        self._kill = False
        self.pendingLine = None
        self.startTime = None

        if autoStart == True:
            self.start()

    def setup(self):
        try:
            self.file = open(self.path, 'r')
            ColorTerminal().success("Opened file %s" % self.path)
        except:
            ColorTerminal().fail("Could not open file %s" % self.path)

        self.startTime = datetime.now()

    def update(self):
        if self.pendingLine == None:
            data = self._nextJsonLine()
        else:
            data = self.pendingLine
            self.pendingLine = None

        if data == None:
            return

        # are we performing frame time-syncs?
        if self.sync:
            # wait until it's time for the next
            dt = self.getTime()
            if data["t"] > dt:
                # store in pendingLine for later processing
                self.pendingLine = data
                return

        for rigid in data['rigidbodies']:
            if self.manager:
                self.manager.processRigidBodyObject({
                    'id': rigid['id'],
                    'position': rigid['p'],
                    'orientation': rigid['r']
                })

    def destroy(self):
        if self.file:
            self.file.close()
        self.file = None
        self.startTime = None

    def setLoop(self, loop):
        self.loop = loop

    def getTime(self):
        if self.startTime is None:
            return 0
        return (datetime.now()-self.startTime).total_seconds()

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
            # print "File does not exist."
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
            self.startTime = datetime.now()
            return self._readLine()

        # nothing (more) to read and we're not looping
        self.stop()
        return None

    def start(self):
        if not self.threaded:
            self.setup()
            return

        if self.thread and self.thread.isAlive():
            ColorTerminal().warn("OscReader - Can't start while a thread is already running")
            return

        self._kill = False
        # threaded loop method will call setup
        self.thread = threading.Thread(target=self.threaded_loop)
        self.thread.start()

    def stop(self):
        if self.threaded:
            # threaded loop method will call destroy
            self._kill = True
        else:
            self.destroy()

    def threaded_loop(self):
        self.setup()

        while not self._kill:
            self.update()

        self.destroy()

    def isRunning(self):
        return self.startTime != None
