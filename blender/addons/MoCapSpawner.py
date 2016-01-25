# blender addon info
bl_info = {
    "name": "MoCap Spawner",
    "author": "Short Notion (Mark van de Korput)",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "location": "View3D > T-panel > Object Tools",
    "description": "Spawns (game) objects to visualize MoCap rigid bodies",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "System"}

# blender python interface
import bpy

# system packages
import logging
import mathutils

# mocap packages
from mocap_bridge.interface.manager import Manager

# this function should be called once (only to initialize) by a game logic controller
def create(controller):
    owner = controller.owner
    MoCapSpawner.for_owner(owner)
    logging.getLogger().info("MoCapSpawner created spawner instance for "+owner.name)


class MoCapSpawner:
    _instances_by_owner = {}

    def for_owner(owner):
        try:
            # Find previously creted instance
            return MoCapSpawner._instances_by_owner[owner]
        except KeyError:
            # Create new instance
            inst = MoCapSpawner(owner)
            # Store it so it can be found next time
            MoCapSpawner._instances_by_owner[owner] = inst
            return inst

    def __init__(self, owner=None):
        self.owner = owner
        self.manager = Manager.instance_by_ref(self.owner) # try to get a global manager instance
        self.config = bpy.data.objects[self.owner.name].moCapSpawnerConfig
        self.rigid_body_object_list = RigidBodyObjectList()

        if self.config.enabled:
            self.manager.addRigidBodiesCallback(self.onRigidBody)

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
            rbo.spawn(self.owner.scene, parent=self.owner, object_name=self.config.object)
            obj = rbo.object

        return obj


# This class manages a single rigid_body-blender_object connection
class RigidBodyObject:
    def __init__(self, rigid_body, object=None):
        self.rigid_body = rigid_body
        self.object=object

    def spawn(self, scene, object_name=None, parent=None):
        if self.object:
            logging.getLogger().warning("RigidBodyObject.spawn replacing existing object")

        if object_name == None:
            object_name = 'Cube'

        self.object = scene.addObject(object_name, object_name)

        if parent:
            self.object.setParent(parent)

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



# This class is in charge of the blender UI config panel
class Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "MoCap Spawner"
    bl_idname = "OBJECT_mocap_spawner"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw_header(self, context):
      layout = self.layout
      config = context.object.moCapSpawnerConfig
      layout.prop(config, "enabled", text='')

    def draw(self, context):
        layout = self.layout
        config = context.object.moCapSpawnerConfig

        if config.enabled == True:
          layout.row().prop(config, "object")


# This class represents the config data (that the UI Panel interacts with)
class Config(bpy.types.PropertyGroup):
  @classmethod
  def register(cls):
    bpy.types.Object.moCapSpawnerConfig = bpy.props.PointerProperty(
      name="MoCapSpawner Config",
      description="Object-specific MoCapSpawner configuration",
      type=cls)

    # Add in the properties
    cls.enabled = bpy.props.BoolProperty(name="enabled", default=False, description="Enable MoCapSpawner for this object")
    cls.object = bpy.props.StringProperty(name="object", default="", description="Object to spawn for every MoCap rigid body")

def register():
  bpy.utils.register_module(__name__)

def unregister():
  bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
  register()
