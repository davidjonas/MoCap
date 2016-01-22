from mocap_bridge.utils.event import Event
from mocap_bridge.interface.manager import Manager

import threading
from datetime import datetime

class ThreadedReader(threading.Thread):
    def __init__(self, manager=None):
        threading.Thread.__init__(self)

        # params
        self.manager = manager

        # attrs
        self.startTime = None
        self.kill = False
        self.daemon = True

        # events
        self.onUpdate = Event()

    # these methods can be overwritten by inheriting classes
    def setup(self): pass
    def destroy(self): pass
    def update(self):
        # this is only for demonstration,
        # and so the inheriting child can call super(<ChildClass>, self).readDataFrame()
        # to trigger the event
        self.onUpdate()

    def run(self):
        self.setup()
        self.kill = False
        self.startTime = datetime.now()
        while not self.kill:
            self.update()
        self.destroy()

    def stop(self):
        self.kill = True

    def getTime(self):
        if self.startTime is None:
            return 0

        return (datetime.now()-self.startTime).total_seconds()
