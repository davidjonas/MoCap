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
            # register callback for new rigid bodies
            # this method will also invoke the callback for any rigid body
            # that is already in the system
            self.manager.addNewRigidBodyCallback(self.onRigidBody)

    # callback method to deal with new rigid bodies
    def onRigidBody(self, rigid_body):
        # spawn blender object and create rigidBody-blenderObject connection record
        self.rigid_body_object_list.add(rigid_body, self.spawnObject())

    def spawnObject(self):
        object = self.owner.scene.addObject(self.config.object, self.config.object)
        object.setParent(self.owner)

        logging.getLogger().debug("RigidBodyObject.spawn spawned new object")
        return object

# This class manages a single rigidBody-blenderObject connection
class RigidBodyObject:
    def __init__(self, rigid_body, object=None):
        self.rigid_body = rigid_body
        self.object=object
        # register callback that gets called whenever the rigid body gets updated
        self.rigid_body.onUpdate += self.onRigidBodyUpdate

    # rigid body update callback
    def onRigidBodyUpdate(self, rigid_body):
        # apply position
        if rigid_body.position:
            self.object.localPosition = rigid_body.position
        # apply orientation
        if rigid_body.orientation:
            self.object.localOrientation = mathutils.Quaternion(rigid_body.orientation)

# This class manages a list of connections between rigid bodies and blender objects
class RigidBodyObjectList:
    def __init__(self):
        self.rigid_body_objects = set()

    def add(self, rigid_body, object=None):
        rbo = RigidBodyObject(rigid_body, object)
        self.rigid_body_objects.add(rbo)
        return rbo

    # not used...
    def remove(self, rigid_body_object):
        try:
            self.rigid_body_objects.remove(rigid_body_object)
        except KeyError:
            pass

    # not used...
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

          mcsObj = MoCapSpawnerObj(context.object)
          # game logic connection not complete; inform user and provide
          # buttons to auto-configure
          if mcsObj.gameLogicConnection() == True:
            layout.row().label(text='Game logic: OK')
          else:
            msgs = []

            if mcsObj.sensor() == None:
              msgs.append('Sensor: NO')
            else:
              msgs.append('Sensor: OK')

            if mcsObj.controller() == None:
              msgs.append('Controller: NO')
            else:
              msgs.append('Controller: OK')

            msgs.append('Connection: NO')
            layout.row().label(text=', '.join(msgs))
            layout.row().operator("object.mocap_spawner_config_game_logic", text="Configure")

# This class provides MoCapSpawner-related information (read-only)
# about a blender object (not a game engine object)
class MoCapSpawnerObj:
    """docstring for """
    def __init__(self, object):
        self.object = object

    def gameLogicConnection(self):
        # if there is no valid sensor, then there can be no connection either
        if self.sensor() == None:
            return False

        # see if the sensor is hooked up to our controller
        # that is assuming there IS a valid controller
        for controller in self.sensor().controllers:
            if controller == self.controller():
                return True

        # no dice
        return False

    def sensor(self):
        # loop through all of this object's game logic sensors
        for sensor in self.object.game.sensors:
            # find one that is appropriately configured
            if sensor.type == 'ALWAYS' and sensor.use_pulse_false_level == False and sensor.use_pulse_true_level == False:
                # return it if found
                return sensor
        # doesn't exist (yet)
        return None

    # returns a controller reference to a appropriaely configured python module controller
    def controller(self):
        for controller in self.object.game.controllers:
            if controller.type == 'PYTHON' and controller.mode == 'MODULE' and controller.module == 'MoCapSpawner.create':
                return controller
        return None

class MoCapSpawnerConfigGameLogicOperator(bpy.types.Operator):
    bl_idname = "object.mocap_spawner_config_game_logic"
    bl_label = "Creates the game logic sensor and controller that requires MoCapSpawner to work"
    bl_description = "Creates an Always sensor and a Python module controller and links them"

    # @classmethod
    # def poll(cls, context):
    #     return True

    def execute(self, context):
      mocap_spawner_obj = MoCapSpawnerObj(context.object)
      if mocap_spawner_obj.controller() == None:
        self.createController(context)

      if mocap_spawner_obj.sensor() == None:
        self.createSensor()

      if mocap_spawner_obj.gameLogicConnection() != True:
        # create the connection
        mocap_spawner_obj.sensor().link(mocap_spawner_obj.controller())

      return {'FINISHED'}

    def createController(self, context):
        print("MoCapSpawner creating Python module controller")
        # create empty PYTHON controller
        bpy.ops.logic.controller_add(type='PYTHON')
        # get reference to newly created controller
        c = context.object.game.controllers[-1]
        # configure appropriately
        c.mode = 'MODULE'
        c.module = 'MoCapSpawner.create'

    def createSensor(self):
        print('MoCapSpawner creating Always sensor')
        # create the sensor
        bpy.ops.logic.sensor_add(type='ALWAYS')


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
