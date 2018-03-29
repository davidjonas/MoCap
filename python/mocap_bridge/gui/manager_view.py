from mocap_bridge.utils.color_terminal import ColorTerminal
from mocap_bridge.interface.manager import Manager

import sys
if sys.version_info[0] >= 3:
    import tkinter as tk
else:
    import Tkinter as tk

class ManagerView:
    def __init__(self, manager=None, parent=None):
        self.manager = manager
        self.parent = parent
        self.setup()

    def setup(self):
        # create a manager if we didn't get an existing manager
        if self.manager == None:
            self.manager = Manager()

        self.frame = tk.LabelFrame(self.parent, text='System', padx=10, pady=10)
        self.frame.grid() #column=0, row=0)

        # create gui-elements
        self.rb_text_label = tk.Label(self.frame, text="Number of Rigid Bodies")
        self.rb_count_label = tk.Label(self.frame, text="0")
        self.reset_button = tk.Button(self.frame, text='reset', command=self.onResetButton)

        # position elements
        self.rb_text_label.grid(column=0, row=0)
        self.rb_count_label.grid(column=1, row=0)
        self.reset_button.grid(column=2, row=0)

        # register callbacks
        self.manager.updateEvent += self.onManagerUpdate

    # calback method; gets called every time anything inside the manager changes
    def onManagerUpdate(self, manager):
        self.rb_count_label.configure(text=str(len(manager.allRigidBodies())))

    def onResetButton(self):
        if self.manager:
            self.manager.reset()
