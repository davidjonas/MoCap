import bpy
import bge

import logging
import mathutils

from mocap_bridge.interface.manager import Manager
from mocap_bridge.readers.json_reader import JsonReader

# this function is called by the game logic controller
def updateMoCap(controller):
    scene = bge.logic.getCurrentScene()

    # first time? Create our main object instanc and attach it to the scene
    if not 'mocap' in scene:
        scene['mocap'] = BlenderMoCap(scene)

    # update our main mocap object
    scene['mocap'].update()

class BlenderMoCap:
    def __init__(self, scene=None):
        print('BlenderMoCap.__init__')

        self.scene = scene

        if self.scene == None:
            self.scene = bge.logic.getCurrentScene()

        self.manager = Manager()
        self.rigid_body_object_list = RigidBodyObjectList()

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
        obj = self.getObject(rigid_body)

        if rigid_body.position:
            obj.localPosition = rigid_body.position
        if rigid_body.orientation:
            obj.localOrientation = mathutils.Quaternion(rigid_body.orientation)

    # finds existing or creates new
    def getObject(self, rigid_body):
        obj = self.rigid_body_object_list.object(rigid_body.id)

        if obj == None:
            rbo = self.rigid_body_object_list.add(rigid_body)
            rbo.spawn(self.scene)
            obj = rbo.object

        return obj

class RigidBodyObject:
    def __init__(self, rigid_body, object=None):
        self.rigid_body = rigid_body
        self.object=object

    def spawn(self, scene, object_name=None):
        if self.object:
            logging.getLogger().warning("RigidBodyObject.spawn replacing existing object")

        if object_name == None:
            object_name = 'Cube' # self.configScene.moCapJsonConfig.

        self.object = scene.addObject(object_name, object_name)
        logging.getLogger().debug("RigidBodyObject.spawn spawned new object")
        return self.object

# This class manages the connection between rigid bodies and blender objects
class RigidBodyObjectList:
    def __init__(self):
        self.rigid_body_objects = set()

    def add(self, param):
        if param.__class__.__name__ == 'RigidBody':
            # turn param in to a RigidBodyObject instance
            param = RigidBodyObject(param)

        self.rigid_body_objects.add(param)
        return param

    def remove(self, rigid_body_object):
        try:
            self.rigid_body_objects.remove(rigid_body_object)
        except KeyError:
            pass

    def object(self, rigid_body_id):
        for rbo in self.rigid_body_objects:
            if rbo.rigid_body.id == rigid_body_id:
                return rbo.object
        return None
