import bpy

from mocap_bridge.interface.manager import Manager
from mocap_bridge.readers.json_reader import JsonReader

class BlenderMoCap:
    # singleton
    _instance = None

    def instance():
        if BlenderMoCap._instance == None:
            BlenderMoCap._instance = BlenderMoCap()

        return BlenderMoCap._instance

    def __init__(self, scene=None):
        self.scene = scene

        if self.scene == None:
            self.scene = bpy.context.scene

        self.manager = Manager()
        # self.osc_reader = OscReader(host=self.scene.moCapOscConfig.host, port= self.scene.moCapOscConfig.port, manager=manager, autoStart=self.scene.moCapOscConfig.enabled)
        self.count = 0

        config = self.scene.moCapJsonConfig
        self.json_reader = JsonReader(path=config.file, loop=config.loop, sync=config.sync, manager=self.manager, autoStart=config.enabled)

    def update(self):
        # if self.osc_reader:
        #     self.osc_reader.update()
        self.count += 1
        print(self.count)
        # print(len(self.manager.allRigidBodies()))

        if self.json_reader and self.scene.moCapJsonConfig.enabled:
            self.json_reader.update()


# from MoCapOSC import BlenderMoCap

BlenderMoCap.instance().update()
