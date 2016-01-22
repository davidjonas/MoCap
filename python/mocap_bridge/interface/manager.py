from mocap_bridge.utils.event import Event
from mocap_bridge.interface.rigid_body import RigidBody
from mocap_bridge.interface.skeleton import Skeleton

class Manager:
    def __init__(self):
        self.rigidbodies = {}
        self.skeletons = {}

        # Events
        self.onUpdate = Event()
        self.onNewSkeleton = Event()
        self.onNewRigidBody = Event()

        self.startTime = None

    #
    # RigidBodies
    #

    def rigidBodyById(self, id):
        try:
            return self.rigid_bodies[id]
        except KeyError:
            return None

    def getOrCreateRigidBody(self, id):
        rigid_body = self.self.rigid_bodies(id)

        if rigid_body == None:
            rigid_body = RigidBodySkeleton(id)
            self.addRigidBody(rigid_body)

        return rigid_body

    # convenience methods, so callers need to know as little
    # as possible about the moca_interface proprietary classes
    def addRigidBodyByObject(self, obj):
        rb = RigidBody().fromObject(obj)
        self.addRigidBody(rigid_body)

    def addRigidBodyByJson(self, json):
        rb = RigidBody().fromJSON(obj)
        self.addRigidBody(rigid_body)

    def addRigidBody(self, rigid_body):
        # TODO check if there was already was a skeleton with this id to trigger update?
        self.rigid_bodies[rigid_body.id] = rigid_body
        self.onNewRigidBody()

    def addOrUpdateRigidBody(self, rigid_body):
        if rigid_body.id in self.rigid_bodies.keys():
            self.rigid_bodies[rb.id].copy(rigid_body)
        else:
            self.rigid_bodies[rb.id] = rb

    #
    # skeletons
    #

    def skeletonById(self, id):
        try:
            return self.skeletons[id]
        except KeyError:
            return None

    def getOrCreateSkeleton(self, id):
        skeleton = self.skeletonById(id)

        if skeleton == None:
            skeleton = Skeleton(id)
            self.addSkeleton(skeleton)

        return skeleton

    def addSkeleton(self, skeleton):
        # TODO check if there was already was a skeleton with this id to trigger update?
        self.skeletons[skeleton.id] = skeleton
        self.onNewSkeleton()
