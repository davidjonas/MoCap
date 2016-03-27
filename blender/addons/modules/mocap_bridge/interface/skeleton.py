# import json
# from mocap_interface.rigid_body import RigidBody

class Skeleton(object):
    def __init__(self, id, rigidbodies={}, name="unnamed"):
        self.id = id
        self.rigid_body_ids = set()
        self.name = name

    def fromObject(self, obj):
        if 'id' in obj:
            self.id = obj["id"]
        elif hasattr(obj, 'id'):
            self.id = obj.id

        if 'name' in obj:
            self.name = obj["name"]
        elif hasattr(obj, 'name'):
            self.name = obj.name

        if 'rigid_body_ids' in obj:
            self.rigid_body_ids = obj["rigid_body_ids"]
        elif hasattr(obj, 'rigid_body_ids'):
            self.rigid_body_ids = set(obj.rigid_body_ids)

        return self

    def toString(self):
        pass

    def toJSON(self):
        pass
