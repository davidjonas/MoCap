from mocap_bridge.interface.marker import Marker
from mocap_bridge.interface.rigid_body import RigidBody
from mocap_bridge.interface.skeleton import Skeleton
from mocap_bridge.utils.event import Event

class BatchesMixin:
    # returns self's batches dict (creates one if necessary)
    def batches(self):
        if hasattr(self, '_batches'):
            return self._batches

        # the batches dict will have the following layout, and will be used to
        # delay event notification until an entire batch has has been completed
        # <batch-identifier>: {
        #   added_rigid_bodies: [<rigid_body>, <rigid_body>],
        #   updated_rigid_bodies: [<rigid_body>, <rigid_body>],
        #   added_skeletons: [<skeleton>, <skeleton>],
        #   updated_skeletons: [<skeleton>, <skeleton>],
        #   markers: [<marker>, <marker>]
        # }
        self._batches = {}

        return self._batches

    # returns the data for a specific batch (creates it if necessary)
    def batch(self, batch_id):
        if not batch_id in self.batches():
            self.batches()[batch_id] = {
                'added_rigid_bodies': set(),
                'updated_rigid_bodies': set(),
                'added_skeletons': set(),
                'updated_skeletons': set(),
                'markers': []
            }

        return self.batches()[batch_id]

    # removes the data for a specific batch (if it exists)
    def removeBatch(self, batch_id):
        if batch_id in self.batches():
            del self.batches()[batch_id]


class Manager(BatchesMixin):
    _instance = None
    _reference_instance = {}

    # for getting a single global instance
    def instance():
        if not Manager._instance:
            Manager._instance = Manager()
        return Manager._instance

    # for creating/getting domain-specific instances
    # ref should identify a specific domain, but can be anything
    def instance_by_ref(ref):
        try:
            return Manager._reference_instance[ref]
        except KeyError:
            inst = Manager()
            Manager._reference_instance[ref] = inst
            return inst

    def __init__(self):
        self.markers = []
        self.rigid_bodies = {}
        self.skeletons = {}

        # Events
        self.updateEvent = Event()
        self.updateMarkersEvent = Event()
        self.updateRigidBodyEvent = Event()
        self.newRigidBodyEvent = Event()

        self.startTime = None
        self.importSkeletonRigidBodies = True

    def finishBatch(self, batch):
        b = self.batch(batch)

        if len(b['markers']) > 0:
            self.markers = b['markers']
            self.updateMarkersEvent(self)

        for rb in b['added_rigid_bodies']:
            self.newRigidBodyEvent(rb)
        for rb in b['updated_rigid_bodies']:
            self.updateRigidBodyEvent(rb)

        # TODO: skeletons
        self.updateEvent(self)
        self.removeBatch(batch)

    # === ===
    # Markers
    # === ===

    def allMarkers(self):
        return self.markers

    def processMarkersData(self, data, batch=None):
        # print('Manager.processMarkersData:', data)
        # reset current list of markers
        self.markers = []

        if batch:
            batch = self.batch(batch) # convert name into batch data container
            # loop over received data (position values) and convert them to marker instances
            for pos in data:
                # add to batch queue
                batch['markers'] += [Marker(pos)]
            return

        # loop over received data (position values) and convert them to marker instances
        for pos in data:
            self.markers += [Marker(pos)]

        # notify the world
        self.updateMarkersEvent(self)
        self.updateEvent(self)

    # === === ===
    # RigidBodies
    # === === ===

    # fetchers
    def allRigidBodies(self):
        return self.rigid_bodies.values()

    def rigidBodyById(self, id):
        try:
            return self.rigid_bodies[id]
        except KeyError:
            return None

    def rigidBodiesBySkeletonId(self, skeleton_id):
        skeleton = self.skeletonById(skeleton_id)
        # map skeleton's rigid body ids to rigid body objects
        rbs = [self.rigidBodyById(rbId) for rbId in skeleton.rigid_body_ids]
        # filter out None values for unfound rigid bodies
        return [rb for rb in rbs if rb]

    def getOrCreateRigidBody(self, id):
        rigid_body = self.rigidBodyById(id)

        if rigid_body == None:
            rigid_body = RigidBody(id)
            self.addRigidBody(rigid_body)

        return rigid_body

    # adders

    def addRigidBody(self, rigid_body, batch=None):
        print('add rb:', rigid_body)
        if rigid_body == None:
            return

        if hasattr(rigid_body, 'id'):
            existing = self.rigidBodyById(rigid_body.id)
        else:
            existing = None

        batch = self.batch(batch) if batch else None

        # UPDATE
        if existing != None:
            # apply changes
            existing.copy(rigid_body)

            if batch:
                # batch; notify later
                batch['updated_rigid_bodies'].add(rigid_body)
            else:
                # no batch; notify now
                self.updateRigidBodyEvent(rigid_body)
        # CREATE
        else:
            # add rigid body
            self.rigid_bodies[rigid_body.id] = rigid_body

            if batch:
                # batch; notify later
                batch['added_rigid_bodies'].add(rigid_body)
            else:
                # no batch; notify now
                self.newRigidBodyEvent(rigid_body)

        if not batch:
            self.updateEvent(self)

    # just an alias with a more explicit name
    def addOrUpdateRigidBody(self, rigid_body, batch=None):
        self.addRigidBody(rigid_body, batch)

    # RAW data processors, these are convenience methods,
    # so the calling class doesn't necessarily have to know
    # about the RigidBody proprietary class

    def processRigidBodyJson(self, json, batch=None):
        rb = RigidBody().fromJSON(json)
        self.addOrUpdateRigidBody(rb, batch)

    def processRigidBodyObject(self, obj, batch=None):
        rb = RigidBody().fromObject(obj)
        # print('Manager processRigidBodyObject, single rb:', rb)
        self.addOrUpdateRigidBody(rb, batch)

    # this is a convenience method that register to given callback
    # for both rigid body create and update events, and also invokes
    # the callback for every rigid body already in the system
    def addRigidBodiesCallback(self, callback):
        self.addNewRigidBodyCallback()
        # also register for rigid body update event
        self.updateRigidBodyEvent += callback

    # this is a convenience method that register to given callback
    # for rigid body create events, and also invokes
    # the callback for every rigid body already in the system
    def addNewRigidBodyCallback(self, callback):
        self.newRigidBodyEvent += callback
        # and invoke callback for every rigid body already in the system
        for rigid_body in self.rigid_bodies:
            callback(rigid_body)

    #
    # skeletons
    #

    # fetchers
    def skeletonById(self, id):
        if id in self.skeletons:
            return self.skeletons[id]
        return None

    def getOrCreateSkeleton(self, id):
        skeleton = self.skeletonById(id)

        if skeleton == None:
            skeleton = Skeleton(id)
            self.addSkeleton(skeleton)

        return skeleton

    # adders
    def addSkeleton(self, skeleton, batch=None):
        existing = self.skeletonById(skeleton.id)
        # turn batch-id into batch data object
        batch = self.batch(batch) if batch else None

        # UPDATE
        if existing != None:
            # apply changes
            existing.copy(skeleton)
        else:
            self.skeletons[skeleton.id] = skeleton #self.skeletonById

        self.updateEvent(self)

        #
        # existing = self.rigidBodyById(rigid_body.id)
        # batch = self.batch(batch) if batch else None
        #
        # # UPDATE
        # if existing != None:
        #     # apply changes
        #     existing.copy(rigid_body)
        #
        #     if batch:
        #         # batch; notify later
        #         batch['updated_rigid_bodies'].add(rigid_body)
        #     else:
        #         # no batch; notify now
        #         self.updateRigidBodyEvent(rigid_body)
        # # CREATE
        # else:
        #     # add rigid body
        #     self.rigid_bodies[rigid_body.id] = rigid_body
        #
        #     if batch:
        #         # batch; notify later
        #         batch['added_rigid_bodies'].add(rigid_body)
        #     else:
        #         # no batch; notify now
        #         self.newRigidBodyEvent(rigid_body)
        #
        # if not batch:
        #     self.updateEvent(self)
        #
        #
        #
        #

    # data transformers
    def processSkeletonObject(self, obj, batch=None):
        sk = Skeleton().fromObject(obj)
        self.addSkeleton(sk, batch)

        if self.importSkeletonRigidBodies and 'rigid_bodies' in obj:
                # print('processSkeletonObject rbs', obj['rigid_bodies'])
                for rb in obj['rigid_bodies']:
                    # print('rb:', rb)
                    # RigidBody(id=327683, position=(0.38059476017951965, 1.168117880821228, -0.10533234477043152), orientation=(-0.1181657463312149, 0.08150681853294373, 0.03866847604513168, -0.988887369632721), markers=[], mrk_ids=(), mrk_sizes=(), mrk_mean_error=-1.0027672160254186e+32, tracking_valid=False))
                    self.processRigidBodyObject({
                        'id': rb.id,
                        'position': rb.position,
                        'orientation': rb.orientation}, batch)
