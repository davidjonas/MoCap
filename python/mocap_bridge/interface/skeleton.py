# import json
# from mocap_interface.rigid_body import RigidBody

class Skeleton(object):
    def __init__(self, id=None, rigidbodies={}, name="unnamed"):
        self.id = id
        self.name = name
        self.rigidbodies=rigidbodies

    def fromObject(self, obj):
        if 'id' in obj:
            self.id = obj["id"]
        elif hasattr(obj, 'id'):
            self.id = obj.id

        if 'name' in obj:
            self.name = obj["name"]
        elif hasattr(obj, 'name'):
            self.name = obj.name

        # TODO; map into our RigidBody class instances?
        if 'rigidbodies' in obj:
            self.rigidbodies = obj['rigidbodies']
        elif hasattr(obj, 'rigidbodies'):
            self.rigidbodies = obj.rigidbodies

        return self

    def copy(self, skeleton):
        self.id = skeleton.id
        self.rigidbodies = skeleton.rigidbodies
        self.name = skeleton.name

    def toString(self):
        pass

    def toJSON(self):
        pass
