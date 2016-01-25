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

from mocap_bridge.interface.manager import Manager
from mocap_bridge.readers.osc_reader import OscReader

# This method should be called by a controller in the blender object's
# game logic and that controller should be triggered by an 'always' sensor,
# with TRUE level triggering enabled (Pulse mode) so it gets called every game-loop iteration
def update(controller):
    owner = controller.owner
    MoCapOsc.for_owner(owner).update()

class MoCapOsc:
    _instances_by_owner = {}

    def for_owner(owner):
        try:
            # Find previously creted instance
            return MoCapOsc._instances_by_owner[owner]
        except KeyError:
            pass

        # Create new instance
        inst = MoCapOsc(owner)
        # Store it so it can be found next time
        MoCapOsc._instances_by_owner[owner] = inst
        return inst

    def __init__(self, owner):
        self.owner = owner
        self.config = bpy.data.objects[self.owner.name].moCapOscConfig
        self.manager = Manager.instance_by_ref(self.owner) # try to get a global manager instance
        try:
            self.reader = OscReader(host=self.config.host, port=self.config.port, manager=self.manager, autoStart=self.config.enabled)
        except NameError:
            self.reader = None
            print("Could not initialize OscReader")

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

def unregister():
  bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
  register()
