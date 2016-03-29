# blender-addon info
bl_info = {
    "name": "MoCap JSON Interface",
    "author": "Short Notion (Mark van de Korput)",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "location": "View3D > T-panel > Object Tools",
    "description": "Receives and processes OSC messages with MoCap data",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "System"}

# blender python interface
import bpy

# MoCapBridge package
from mocap_bridge.interface.manager import Manager
from mocap_bridge.readers.json_reader import JsonReader

# This method should be called by a controller in the blender object's
# game logic and that controller should be triggered by an 'always' sensor,
# with TRUE level triggering enabled (Pulse mode) so it gets called every game-loop iteration
def update(controller):
    owner = controller.owner
    MoCapJson.for_owner(owner).update()


class MoCapJson:
    _instances_by_owner = {}

    def for_owner(owner):
        try:
            # Find previously creted instance
            return MoCapJson._instances_by_owner[owner]
        except KeyError:
            # Create new instance
            inst = MoCapJson(owner)
            # Store it so it can be found next time
            MoCapJson._instances_by_owner[owner] = inst
            return inst

    def __init__(self, owner):
        self.owner = owner
        self.config = bpy.data.objects[self.owner.name].moCapJsonConfig
        self.manager = Manager.instance_by_ref(self.owner) # try to get a global manager instance
        self.json_reader = JsonReader(path=self.config.file, loop=self.config.loop, sync=self.config.sync, manager=self.manager, autoStart=self.config.enabled)

    def update(self):
        if self.config.enabled:
            self.json_reader.update()
            # print("JSON time: {0}".format(self.json_reader.getTime()))


# This class is in charge of the blender UI config panel
class Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "MoCap JSON"
    bl_idname = "OBJECT_mocap_json"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw_header(self, context):
      layout = self.layout
      config = context.object.moCapJsonConfig
      layout.prop(config, "enabled", text='')

    def draw(self, context):
        layout = self.layout
        config = context.object.moCapJsonConfig

        if config.enabled == True:
            layout.row().prop(config, "file")
            layout.row().prop(config, "loop")
            layout.row().prop(config, "sync")

            mcjObj = MoCapJsonObj(context.object)
            # game logic connection not complete; inform user and provide
            # buttons to auto-configure
            if mcjObj.gameLogicConnection() == True:
              layout.row().label(text='Game logic: OK')
            else:
              msgs = []

              if mcjObj.sensor() == None:
                msgs.append('Sensor: NO')
              else:
                msgs.append('Sensor: OK')

              if mcjObj.controller() == None:
                msgs.append('Controller: NO')
              else:
                msgs.append('Controller: OK')

              msgs.append('Connection: NO')
              layout.row().label(text=', '.join(msgs))
              layout.row().operator("object.mocap_json_config_game_logic", text="Configure")


# This class provides MoCapJson-related information (read-only)
# about a blender object (not a game engine object)
class MoCapJsonObj:
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
            if sensor.type == 'ALWAYS' and sensor.use_pulse_false_level == False and sensor.use_pulse_true_level == True:
                # return it if found
                return sensor
        # doesn't exist (yet)
        return None

    # returns a controller reference to a appropriaely configured python module controller
    def controller(self):
        for controller in self.object.game.controllers:
            if controller.type == 'PYTHON' and controller.mode == 'MODULE' and controller.module == 'MoCapJSON.update':
                return controller
        return None

class MoCapJsonConfigGameLogicOperator(bpy.types.Operator):
    bl_idname = "object.mocap_json_config_game_logic"
    bl_label = "Creates the game logic sensor and controller that requires MoCapJSON to work"
    bl_description = "Creates an Always sensor and a Python module controller and links them"

    # @classmethod
    # def poll(cls, context):
    #     return True

    def execute(self, context):
      obj = MoCapJsonObj(context.object)
      if obj.controller() == None:
        self.createController(context)

      if obj.sensor() == None:
        self.createSensor(context)

      if obj.gameLogicConnection() != True:
        # create the connection
        print("MoCapJSON creating game logic link")
        obj.sensor().link(obj.controller())

      return {'FINISHED'}

    def createController(self, context):
        print("MoCapJSON creating Python module controller")
        # create empty PYTHON controller
        bpy.ops.logic.controller_add(type='PYTHON')
        # get reference to newly created controller
        c = context.object.game.controllers[-1]
        # configure appropriately
        c.mode = 'MODULE'
        c.module = 'MoCapJSON.update'

    def createSensor(self, context):
        print('MoCapJSON creating Always sensor')
        # create the sensor
        bpy.ops.logic.sensor_add(type='ALWAYS')
        # get reference to newly created sensor
        s = context.object.game.sensors[-1]
        s.use_pulse_true_level = True

# This class represents the config data (that the UI Panel interacts with)
class Config(bpy.types.PropertyGroup):
  @classmethod
  def register(cls):
    bpy.types.Object.moCapJsonConfig = bpy.props.PointerProperty(
      name="MoCapJSON Config",
      description="Object-specific MoCapOSC connection configuration",
      type=cls)

    # Add in the properties
    cls.enabled = bpy.props.BoolProperty(name="enabled", default=False, description="Enable MoCapJSON")
    cls.file = bpy.props.StringProperty(name="file", default="mocap.json")
    cls.loop = bpy.props.BoolProperty(name="loop", default=True, description="Loop back to start after reaching the end of the json mocap data")
    cls.sync = bpy.props.BoolProperty(name="sync", default=True, description="Synchronise mocap data using the embedded timestamps")


def register():
  bpy.utils.register_module(__name__)

def unregister():
  bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
  register()
