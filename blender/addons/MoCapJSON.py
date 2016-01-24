bl_info = {
    "name": "MoCap JSON Interface",
    "author": "Short Notion (Mark van de Korput)",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "location": "View3D > T-panel > Scene Tools",
    "description": "Receives and precosses OSC messages with MoCap data",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "System"}

# system stuff
import logging
# blender stuff
import bpy

# This class is in charge of the blender UI config panel
class Panel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "MoCap JSON"
    bl_idname = "SCENE_mocap_json"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw_header(self, context):
      layout = self.layout
      config = context.scene.moCapJsonConfig
      layout.prop(config, "enabled", text='')

    def draw(self, context):
        layout = self.layout
        config = context.scene.moCapJsonConfig

        if config.enabled == True:
          layout.row().prop(config, "file")
          layout.row().prop(config, "loop")
          layout.row().prop(config, "sync")


# This class represents the config data (that the UI Panel interacts with)
class Config(bpy.types.PropertyGroup):
  @classmethod
  def register(cls):
    bpy.types.Scene.moCapJsonConfig = bpy.props.PointerProperty(
      name="MoCapJSON Config",
      description="Scene-specific MoCapOSC connection configuration",
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
