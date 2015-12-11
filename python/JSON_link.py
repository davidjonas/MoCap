from terminal_colors import bcolors
import sys
import json
from event import Event
from datetime import datetime

class JSONLink:
    """
    JSON link to record json translated MoCap data from NatNet
    """

    def __init__(self, natnet=None, path=None, autoStart=False):
        # params
        self.natnet = natnet
        self.path = path
        self.autoStart=autoStart

        # attributes
        self.startTime = None
        self.recordedFrames = 0
        self.file = None

        if self.path == None:
            # default path: timestamped natnet_<timestamp>.json
            self.path = "data/natnet_"+datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+".json"

        if self.autoStart == True:
            self.start()

    def start(self):
        if self.natnet:
            self.natnet.updated += self.onNatNetUpdate
            self.startTime = datetime.now()

        self.file = open(self.path, 'wb')
        # add a comment with data formatting disclaimer at the start of the file
        self.file.write('# JSON data recorded from natnet parser, see: https://github.com/davidjonas/MoCap/tree/master/python\n')
        self.file.write('# FORMAT: each line in the file represents a frame of natnet data and should be parsed independently from the other lines\n')

    def stop(self):
        if self.natnet:
            self.natnet.updated -= self.onNatNetUpdate

        if self.file:
            self.file.write(']}')
            self.file.close()
            self.file = None

    def onNatNetUpdate(self):
        t = datetime.now()
        dt = (t-self.startTime).total_seconds()
        data = self._frameData(dt)
        # note: we're not storing strictly correct data; each line is valid json on its own,
        # but together they are not wrapped inside an element (or comma seperated)
        self.file.write(data+"\n")
        self.recordedFrames = self.recordedFrames+1
        print("[JSONLink] recorded "+str(self.recordedFrames)+" frames in "+str(dt)+" seconds ("+str(self.recordedFrames/dt)+" fps)")


    def _frameData(self, timestamp):
        # print("TODO: saveFrame with timestamp (microseconds): "+str(timestamp))

        data = {
            't': timestamp,
            'rigidbodies': [
            ]
        }

        for rb in self.natnet.rigidbodies:
            data['rigidbodies'].append({
                'id': rb.id,
                'p': rb.position,
                'r': rb.orientation
            })
        
        return json.dumps(data)

        

