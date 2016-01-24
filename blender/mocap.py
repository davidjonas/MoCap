import bpy
import bge

import logging
import mathutils

from mocap_bridge.interface.manager import Manager
from mocap_bridge.readers.json_reader import JsonReader

# this function is called by the game logic controller
def updateMoCap(controller):
    scene = bge.logic.getCurrentScene()
    MoCap.for_scene(scene).update()
    if not 'mocapjson' in scene:
        scene['mocapjson'] = MoCapJson()
    scene['mocapjson'].update()

class MoCap:
    def for_scene(scene):
        if not 'mocap' in scene:
            scene['mocap'] = MoCap(scene)
        return scene['mocap']

    def __init__(self, scene=None):
        self.scene = scene

        if self.scene == None:
            self.scene = bge.logic.getCurrentScene()

        self.manager = Manager.instance()
        self.rigid_body_object_list = RigidBodyObjectList()

        self.manager.addRigidBodiesCallback(self.onRigidBody)
        self.manager.processRigidBodyObject({'id': 1, 'position': (0.0, 0.0, 0.0), 'orientation': (0.0, 0.0, 0.0, 0.0)})

    def update(self):
        pass

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

class MoCapJson:
    def __init__(self, scene=None, manager=None):
        self.scene = scene
        if self.scene == None:
            self.scene = bpy.context.scene

        self.manager = manager
        if not self.manager:
            self.manager = Manager.instance()

        config = self.scene.moCapJsonConfig
        self.json_reader = JsonReader(path=config.file, loop=config.loop, sync=config.sync, manager=self.manager, autoStart=config.enabled)

    def update(self):
        if self.json_reader and self.scene.moCapJsonConfig.enabled:
            self.json_reader.update()

class RigidBodyObject:
    def __init__(self, rigid_body, object=None):
        self.rigid_body = rigid_body
        self.object=object

    def spawn(self, scene, object_name=None):
        if self.object:
            logging.getLogger().warning("RigidBodyObject.spawn replacing existing object")

        if object_name == None:
            object_name = 'Cube'

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
