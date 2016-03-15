from mocap_bridge.utils.color_terminal import ColorTerminal
from mocap_bridge.interface.manager import Manager
import Tkinter

class ManagerView:
    def __init__(self, manager=None, tk=None):
        self.manager = manager
        self.tk = tk
        self.setup()

    def setup(self):
        # create a manager if we didn't get an existing manager
        if self.manager == None:
            self.manager = Manager()

        # create and configure view container if we didn't get an existing container
        if self.tk == None:
            self.tk = Tkinter.Tk()
            self.tk.title('MoCap Manager')
            # self.tk.geometry('1000x330')

        # create gui-elements
        self.frame = Tkinter.Frame(self.tk, padx=50, pady=50)
        self.rb_text_label = Tkinter.Label(self.frame, text="Number of Rigid Bodies")
        self.rb_count_label = Tkinter.Label(self.frame, text="0")
        # position elements
        self.frame.grid(column=0, row=0)
        self.rb_text_label.grid(column=0, row=0)
        self.rb_count_label.grid(column=1, row=0)

        # register callbacks
        self.manager.updateEvent += self.onManagerUpdate

    def update(self):
        if self.tk:
            try:
                self.tk.update()
                return True
            except:
                self.destroy()
                return False

    def destroy(self):
        self.tk = None

    # calback method; gets called every time anything inside the manager changes
    def onManagerUpdate(self, manager):
        if self.tk:
            try:
                self.rb_count_label.configure(text=str(len(manager.allRigidBodies())))
            except:
                self.destroy()
