import json
from datetime import datetime

class JsonWriter:
    def __init__(self, path=None, manager=None, recordRigidBodies=True, recordMarkers=True, autoStart=True):
        # params
        self.path = path
        self.manager = manager
        self.recordRigidBodies = recordRigidBodies
        self.recordMarkers = recordMarkers

        if self.path == None:
            # default path: timestamped natnet_<timestamp>.json
            self.path = "data/natnet_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".json"

        # attributes
        self.startTime = None
        self.recordedFrames = 0
        self.file = None

        if autoStart == True:
            self.start()

    def start(self):
        # open output file
        self.file = open(self.path, 'wb')

        # add comments with data formatting disclaimer at the start of the file
        self.file.write('# MoCap NatNet JSON data recorded from using JsonWriter, see: https://github.com/davidjonas/MoCap/tree/master/python\n')
        self.file.write('# FORMAT: each line in the file represents a frame of natnet data and should be parsed independently from the other lines\n')

        self.startTime = datetime.now()

        # register manager update callback
        if self.manager != None:
            # the event class already discards duplicates, so no need to check
            self.manager.updateEvent += self.onManagerUpdate

    def stop(self):
        # unregister manager callback
        if self.manager:
            self.manager.updateEvent -= self.onManagerUpdate

        # close output file
        if self.file:
            self.file.close()
            self.file = None

    def onManagerUpdate(self, manager):
        # we'll need an open output file handle, if we don't have it; abort
        if not self.file:
            return

        t = datetime.now() # current time
        dt = (t-self.startTime).total_seconds() # time (in seconds) since we started recorded
        data = self._frameJson(dt) # current frame as json data

        # note: we're not storing strictly correct data; each line is valid json on its own,
        # but together they are not wrapped inside an element (or comma seperated)
        self.file.write(data+"\n")
        self.recordedFrames = self.recordedFrames+1
        print("[JSONLink] recorded "+str(self.recordedFrames)+" frames in "+str(dt)+" seconds ("+str(self.recordedFrames/dt)+" fps)")

    def _frameJson(self, timestamp):
        data = {
            't': timestamp,
        }

        if self.recordMarkers:
            data['markers'] = map(lambda marker: marker.position, self.manager.markers)

        if self.recordRigidBodies:
            data['rigidbodies'] = []
            for rb in self.manager.allRigidBodies():
                data['rigidbodies'].append({
                    'id': rb.id,
                    'p': rb.position,
                    'r': rb.orientation
                })

        return json.dumps(data)
