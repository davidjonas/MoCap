import json
from event import Event

class RigidBody(object):
    def __init__(self, id=None, position=None, orientation=None, obj=None, name="unnamed"):
        if obj is None and id is not None and position is not None and orientation is not None:
            self.id = id
            self.position = position
            self.orientation = orientation
            self.name = name
        elif obj is not None:
            self.fromObject(obj)
        self.onUpdate = Event()

    def update(self, position, orientation):
        self.position = position
        self.orientation = orientation
        self.onUpdate()

    def rename(self, name):
        self.name = name

    def toString(self):
        return "%(name)s () = p(%(posX)s, %(posY)s, %(posZ)s), r(%(rotX)s, %(rotY)s, %(rotZ)s, %(rotW)s)" % {
            "name": self.name,
            "id": self.id,
            "posX": self.position[0],
            "posY": self.position[1],
            "posZ": self.position[2],
            "rotX": self.orientation[0],
            "rotY": self.orientation[1],
            "rotZ": self.orientation[2],
            "rotW": self.orientation[3]
        }

    def toObject(self):
        return {
            "id": self.id,
            "name": self.name,
            "position": self.position,
            "orientation": self.orientation
        }

    def fromObject(self, obj):
        self.id = obj["id"]
        self.position = obj["position"]
        self.orientation = obj["orientation"]
        self.name = obj["name"]

    def toJSON(self):
        json_obj = self.toObject()
        return json.dumps(json_obj)

    def fromJSON(self, raw_json):
        json_data = json.loads(raw_json)
        self.fromObject(json_data)
        return self
