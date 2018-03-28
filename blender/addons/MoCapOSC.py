bl_info = {
    "name": "MoCap OSC Interface",
    "author": "Short Notion (Mark van de Korput)",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "location": "View3D > T-panel > Object Tools",
    "description": "Receives and processes OSC messages with MoCap data",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "System"}

# blender stuff
import bpy
from bpy.app.handlers import persistent

# mocap stuff
from mocap_bridge.interface.manager import Manager
from mocap_bridge.readers.osc_reader import OscReader


# This method should be called by a controller in the blender object's
# game logic and that controller should be triggered by an 'always' sensor,
# with TRUE level triggering enabled (Pulse mode) so it gets called every game-loop iteration
def update(controller):
    MoCapOsc.for_owner(controller.owner).update()

# This method is called by the game_post handler (registered at the bottom of this file)
@persistent
def cleanup(scene):
    print("MoCapOSC.cleanup")
    MoCapOsc.remove_owner_instances()

class MoCapOsc:

    #
    # Class
    #

    _owner_instances = set()

    def for_owner(owner):
        # Find previously created instance
        for instance in MoCapOsc._owner_instances:
            if instance.owner == owner:
                return instance
        # Create new instance
        instance = MoCapOsc(owner)
        MoCapOsc._owner_instances.add(instance)
        return instance

    def remove_owner_instance(instance):
        try:
            MoCapOsc._owner_instances.remove(instance)
        except KeyError:
            print("MoCapOsc.remove_owner_instance asked to remove unknown instance of MoCapOsc")

    def remove_owner_instances():
        MoCapOsc._owner_instances.clear()

    #
    # Instance
    #

    def __init__(self, owner):
        self.owner = owner
        self.config = bpy.data.objects[self.owner.name].moCapOscConfig
        self.manager = Manager.instance_by_ref(self.owner) # try to get a global manager instance

        try:
            self.reader = OscReader(host=self.config.host, port=self.config.port, manager=self.manager, autoStart=self.config.enabled)
        except NameError as err:
            self.reader = None
            print("Could not initialize OscReader:")
            print(err)

    # destructor; gets called when the life-cycle of this instance ends
    def __del__(self):
        # this makes sure the OSC socket connection gets freed up
        self.destroy()

    def destroy(self):
        if self.reader:
            self.reader.stop()
            self.reader = None

    def update(self):
        if self.reader and self.config.enabled:
            self.reader.update()


# This class is in charge of the blender UI config panel
class Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "MoCap OSC"
    bl_idname = "OBJECT_mocap_osc"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw_header(self, context):
      layout = self.layout
      config = context.object.moCapOscConfig
      layout.prop(config, "enabled", text='')

    def draw(self, context):
        layout = self.layout
        config = context.object.moCapOscConfig

        if config.enabled == True:
            layout.row().prop(config, "host")
            layout.row().prop(config, "port")

            mcoObj = MoCapOscObj(context.object)
            # game logic connection not complete; inform user and provide
            # buttons to auto-configure
            if mcoObj.gameLogicConnection() == True:
              layout.row().label(text='Game logic: OK')
            else:
              msgs = []

              if mcoObj.sensor() == None:
                msgs.append('Sensor: NO')
              else:
                msgs.append('Sensor: OK')

              if mcoObj.controller() == None:
                msgs.append('Controller: NO')
              else:
                msgs.append('Controller: OK')

              msgs.append('Connection: NO')
              layout.row().label(text=', '.join(msgs))
              layout.row().operator("object.mocap_osc_config_game_logic", text="Configure")


# This class provides MoCapOSC-related information (read-only)
# about a blender object (not a game engine object)
class MoCapOscObj:
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
            if controller.type == 'PYTHON' and controller.mode == 'MODULE' and controller.module == 'MoCapOSC.update':
                return controller
        return None

class MoCapOscConfigGameLogicOperator(bpy.types.Operator):
    bl_idname = "object.mocap_osc_config_game_logic"
    bl_label = "Creates the game logic sensor and controller that requires MoCapOSC to work"
    bl_description = "Creates an Always sensor and a Python module controller and links them"

    # @classmethod
    # def poll(cls, context):
    #     return True

    def execute(self, context):
      obj = MoCapOscObj(context.object)
      if obj.controller() == None:
        self.createController(context)

      if obj.sensor() == None:
        self.createSensor(context)

      if obj.gameLogicConnection() != True:
        # create the connection
        print("MoCapOSC creating game logic link")
        obj.sensor().link(obj.controller())

      return {'FINISHED'}

    def createController(self, context):
        print("MoCapOSC creating Python module controller")
        # create empty PYTHON controller
        bpy.ops.logic.controller_add(type='PYTHON')
        # get reference to newly created controller
        c = context.object.game.controllers[-1]
        # configure appropriately
        c.mode = 'MODULE'
        c.module = 'MoCapOSC.update'

    def createSensor(self, context):
        print('MoCapOSC creating Always sensor')
        # create the sensor
        bpy.ops.logic.sensor_add(type='ALWAYS')
        # get reference to newly created sensor
        s = context.object.game.sensors[-1]
        s.use_pulse_true_level = True


# This class represents the config data (that the UI Panel interacts with)
class Config(bpy.types.PropertyGroup):
  @classmethod
  def register(cls):
    bpy.types.Object.moCapOscConfig = bpy.props.PointerProperty(
      name="MoCapOSC Config",
      description="Object-specific MoCapOSC connection configuration",
      type=cls)

    # Add in the properties
    cls.enabled = bpy.props.BoolProperty(name="enabled", default=False, description="Enable MoCapOSC")
    cls.host = bpy.props.StringProperty(name="OSC Host", default="127.0.0.1")
    cls.port = bpy.props.IntProperty(name="OSC Port", default=8080, soft_min=0)

def register():
  bpy.utils.register_module(__name__)
  bpy.app.handlers.game_post.append(cleanup)

def unregister():
  bpy.utils.unregister_module(__name__)
  bpy.app.handlers.game_post.remove(cleanup)

if __name__ == "__main__":
  register()
