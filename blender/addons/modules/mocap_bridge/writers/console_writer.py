# This class is mostly for debugging and testing

from mocap_bridge.utils.color_terminal import ColorTerminal
from datetime import datetime

class ConsoleWriter:
    def __init__(self, manager=None, delay=0.5, autoStart=True):
        # params
        self.setManager(manager)
        self.delay=delay

        # attributes
        self.startTime = None
        self.lastUpdateTime = None

        if autoStart == True:
            self.start()

    def start(self):
        self.startTime = datetime.now()

    def stop(self):
        self.startTime = None

    def setManager(self, manager):
        if hasattr(self, 'manager') and self.manager:
            self.manager.updateEvent -= self.onUpdate

        self.manager = manager

        if self.manager: # could also be None
            self.manager.updateEvent += self.onUpdate

    def isRunning(self):
        return self.startTime != None

    def onUpdate(self, manager):
        if not self.isRunning():
            return

        t = self.getTime()

        if self.delay != None and self.lastUpdateTime != None and t < (self.lastUpdateTime + self.delay):
            return

        line = "{0}: {1} markers, {2} rigid bodies and {3} skeletons".format(t, len(manager.markers), len(manager.rigid_bodies), len(manager.skeletons))
        print(line)
        for marker in manager.allMarkers():
            print(marker.position)
        self.lastUpdateTime = t

    def getTime(self):
        if self.startTime is None:
            return 0

        return (datetime.now()-self.startTime).total_seconds()
