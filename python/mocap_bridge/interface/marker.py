import json
from mocap_bridge.utils.event import Event
from mocap_bridge.utils.color_terminal import ColorTerminal

class Marker(object):
    def __init__(self, position=None):
        self.position = position

    def copy(self, marker):
        self.update(marker.position)

    def update(self, position):
        self.position = position

    def toString(self):
        return "marker: (%(posX)s, %(posY)s, %(posZ)s)" % {
            "posX": self.position[0],
            "posY": self.position[1],
            "posZ": self.position[2],
        }
