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

    def toObject(self):
        return {
            "position": self.position
        }

    def fromObject(self, obj):
        if not 'keys' in dir(obj):
            ColorTerminal().red('Marker.fromObject received non-dict object')
            return

        if 'position' in obj.keys():
            self.position = obj["position"]

        return self

    def toJSON(self):
        json_obj = self.toObject()
        return json.dumps(json_obj)

    def fromJSON(self, raw_json):
        json_data = json.loads(raw_json)
        self.fromObject(json_data)
        return self
