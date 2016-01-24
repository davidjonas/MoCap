import bpy
import bge

import mathutils
# import math

from mocap_bridge.interface.manager import Manager
from mocap_bridge.readers.json_reader import JsonReader

# this function is called by the game logic controller
def updateMoCap(controller):
    BlenderMoCap.instance().update()

class BlenderMoCap:
    # singleton
    _instance = None

    def instance():
        if BlenderMoCap._instance == None:
            BlenderMoCap._instance = BlenderMoCap()

        return BlenderMoCap._instance

    def __init__(self, scene=None):
        self.scene = scene

        if self.scene == None:
            self.scene = bge.logic.getCurrentScene()

        self.manager = Manager()
        self.rigid_body_objects = RigidBodyObjects(self.scene)

        # self.osc_reader = OscReader(host=self.scene.moCapOscConfig.host, port= self.scene.moCapOscConfig.port, manager=manager, autoStart=self.scene.moCapOscConfig.enabled)
        self.configScene = bpy.context.scene
        config = self.configScene.moCapJsonConfig
        self.json_reader = JsonReader(path=config.file, loop=config.loop, sync=config.sync, manager=self.manager, autoStart=config.enabled)

        self.manager.addRigidBodiesCallback(self.onRigidBody)
        self.manager.processRigidBodyObject({'id': 1, 'position': (0.0, 0.0, 0.0), 'orientation': (0.0, 0.0, 0.0, 0.0)})

    def update(self):
        if self.json_reader and self.configScene.moCapJsonConfig.enabled:
            self.json_reader.update()

    def onRigidBody(self, rigid_body):
        print("Got rigid body, id: {0}".format(rigid_body.id))
        obj = self.getObject(rigid_body)

        if rigid_body.position:
            obj.localPosition = rigid_body.position
        # if rigid_body.orientation:
        #     print(rigid_body.orientation)
        #     obj.localOrientation = mathutils.Quaternion(rigid_body.orientation)

    # finds existing or creates new
    def getObject(self, rigid_body):
        obj = self.rigid_body_objects.object(rigid_body.id)

        if obj == None:
            obj = self.spawnObject()
            self.rigid_body_objects.add(rigid_body, obj.name)

        return obj

    def spawnObject(self, object_name=None):
        if object_name == None:
            object_name = 'Cube' # self.configScene.moCapJsonConfig.

        return self.scene.addObject(object_name, object_name)



# This class manages the connection between rigid bodies and blender objects
class RigidBodyObjects:
    def __init__(self, scene=None):
        # mapping will hold <rigid_body ID>: <object_name> pairs
        self.mapping = {}
        self.rigid_bodies = set()

        self.scene = scene
        if not self.scene:
            self.scene = bge.logic.getCurrentScene()

    def add(self, rigid_body, object_name):
        self.mapping[rigid_body.id] = object_name
        self.rigid_bodies.add(rigid_body)

    def remove(self, rigid_body):
        try:
            self.mapping.pop(rigid_body.id)
        except KeyError:
            pass

        # the given rigid body might be a different
        # instance with the same id
        rb = self.rigid_body_by_id(rigid_body.id)

        if rb != None:
            self.rigid_bodies.remove(rb)

    def object_name(self, rigid_body_id):
        try:
            return self.mapping[rigid_body_id]
        except KeyError:
            return None

    def object(self, rigid_body_id):
        name = self.object_name(rigid_body_id)
        if name:
            return self.scene.objects[name]
        return None

    def rigid_body_id(self, object_name):
        for rigid_body_id, obj_name in self.mapping.iteritems():
            if obj_name == object_name:
                return rigid_body_id
        return None

    def rigid_body(self, object_name):
        return self.rigid_body_by_id(self.rigid_body_id(object_name))

    def rigid_body_by_id(self, rigid_body_id):
        for rigid_body in self.rigid_bodies:
            if rigid_body.id == id:
                return rigid_body
        return None

# from MoCapOSC import BlenderMoCap
