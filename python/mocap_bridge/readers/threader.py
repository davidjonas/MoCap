from mocap_bridge.utils.event import Event

import threading
from datetime import datetime

class Threader(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # attrs
        self.startTime = None
        self.kill = False
        self.daemon = True

        # events
        self.onSetup = Event()
        self.onUpdate = Event()
        self.onDestroy = Event()

    def run(self):
        self.onSetup()
        self.kill = False
        self.startTime = datetime.now()
        while not self.kill:
            self.onUpdate()
        self.onDestroy()

    def stop(self):
        self.kill = True

    def getTime(self):
        if self.startTime is None:
            return 0

        return (datetime.now()-self.startTime).total_seconds()
