bl_info = {
    "name": "MoCap Interface Core",
    "author": "Short Notion (Mark van de Korput)",
    "version": (0, 1),
    "blender": (2, 75, 0),
    "location": "View3D > T-panel > Scene Tools",
    "description": "Receives and processes OSC messages with MoCap data",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "System"}

# system stuff
import logging
# blender stuff
import bpy

from mocap_bridge.interface.manager import Manager

class MoCapCore:
    def for_owner(owner):
        if not 'mocap' in owner:
            owner['mocap'] = MoCapCore(owner)
        return owner['mocap']

    def __init__(self, owner):
        self.owner = owner
        self.manager = Manager()


def register():
  # bpy.utils.register_module(__name__)
  pass

def unregister():
  # bpy.utils.unregister_module(__name__)
  pass

if __name__ == "__main__":
  register()
