import json
from mocap_bridge.utils.event import Event
from mocap_bridge.utils.color_terminal import ColorTerminal

class RigidBody(object):
    def __init__(self, id=None, position=None, orientation=None, name="unnamed", obj=None):
        self.id = id
        self.position = position
        self.orientation = orientation
        self.name = name

        if obj is not None:
            self.fromObject(obj)

        self.onUpdate = Event()

    def copy(self, rigid_body):
        self.update(rigid_body.position, rigid_body.orientation)

    def update(self, position, orientation):
        self.position = position
        self.orientation = orientation
        self.onUpdate(self)

    def rename(self, name):
        self.name = name
        # self.onUpdate ???

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

    def toJSON(self):
        json_obj = self.toObject()
        return json.dumps(json_obj)

    def fromObject(self, obj):
        # print('RigidBody.fromObject, got:', obj)

        # properties object
        if not 'keys' in dir(obj):
            # ColorTerminal().red('RigidBody.fromObject received non-dict object')
            if hasattr(obj, 'id'):
                self.id = obj.id
            if hasattr(obj,'position'):
                self.position = obj.position
            if hasattr(obj, 'orientation'):
                self.orientation = obj.orientation
            if hasattr(obj, 'name'):
                self.name = obj.name
            return self

        # dict
        if 'id' in obj.keys():
            self.id = obj["id"]
        if 'position' in obj.keys():
            self.position = obj["position"]
        if 'orientation' in obj.keys():
            self.orientation = obj["orientation"]
        if 'name' in obj.keys():
            self.name = obj["name"]

    def toJSON(self):
        json_obj = self.toObject()
        return json.dumps(json_obj)

    def fromJSON(self, raw_json):
        json_data = json.loads(raw_json)
        self.fromObject(json_data)
        return self
