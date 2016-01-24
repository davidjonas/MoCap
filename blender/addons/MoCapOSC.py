bl_info = {
    "name": "MoCap OSC Interface",
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
    bl_label = "MoCap OSC"
    bl_idname = "SCENE_mocap_osc"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw_header(self, context):
      layout = self.layout
      config = context.scene.moCapOscConfig
      layout.prop(config, "enabled", text='')

    def draw(self, context):
        layout = self.layout
        config = context.scene.moCapOscConfig

        if config.enabled == True:
          layout.row().prop(config, "host")
          layout.row().prop(config, "port")

# end of class PointCloudLoaderPanel


# This class represents the config data (that the UI Panel interacts with)
class Config(bpy.types.PropertyGroup):
  @classmethod
  def register(cls):
    bpy.types.Scene.moCapOscConfig = bpy.props.PointerProperty(
      name="MoCapOSC Config",
      description="Scene-specific MoCapOSC connection configuration",
      type=cls)

    # Add in the properties
    cls.enabled = bpy.props.BoolProperty(name="enabled", default=False, description="Enable MoCapOSC")
    cls.host = bpy.props.StringProperty(name="OSC Host", default="127.0.0.1")
    cls.port = bpy.props.IntProperty(name="OSC Port", default=8080, soft_min=0)

  ## Unregister is causing errors and doesn't seem to be necessary
  # @classmethod
  # def unregister(cls):
  #   print("Unreg: ")
  #   print(dir(bpy.types.Object))
  #   del bpy.types.Object.pointCloudLoaderConfig



def register():
  bpy.utils.register_module(__name__)

def unregister():
  bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
  register()
