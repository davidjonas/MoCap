# import json
# from mocap_interface.rigid_body import RigidBody

class Skeleton(object):
    def __init__(self, skelid, rigidbodies={}, name="unnamed"):
        self.id = skelid
        self.rigidbodies = rigidbodies
        self.name = name

    def addRigidbody(self, rb):
        self.rigidbodies[rb.id] = rb

    def getRigidbody(self, rbid):
        if rbid in self.rigidbodies.keys():
            return self.rigidbodies[rbid]
        return None

    def addOrUpdateRigidbody(self, rb):
        if rb.id in self.rigidbodies.keys():
            self.rigidbodies[rb.id].update(rb.position, rb.orientation)
        else:
            self.rigidbodies[rb.id] = rb


    def toString(self):
        pass

    def toJSON(self):
        pass
