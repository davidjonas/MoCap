from mocap_bridge.writers.osc_writer import OscWriter

import Tkinter as tk

class OscWriterView:
    def __init__(self, osc_writer=None, parent=None):
        self.osc_writer = osc_writer
        self.parent = parent

        if self.osc_writer == None:
            self.osc_writer = OscWriter()

        self.setup()

    def setup(self):
        # create gui-elements
        self.frame = tk.Frame(self.parent, padx=10, pady=10)
        self.frame.grid()

        self.host_label = tk.Label(self.frame, text="OSC Host")
        self.host_entry = tk.Entry(self.frame, width=10)
        self.port_label = tk.Label(self.frame, text="Port")
        self.port_entry = tk.Entry(self.frame, width=5)
        self.connect_button = tk.Button(self.frame, text='connect', command=self.onConnect)
        self.connect_button.grid(column=1, row=0)

        # position elements
        self.host_label.grid(column=0, row=0)
        self.host_entry.grid(column=1, row=0)
        self.port_label.grid(column=2, row=0)
        self.port_entry.grid(column=3, row=0)
        self.connect_button.grid(column=4, row=0)

        # initialize
        if self.osc_writer:
            self.host_entry.insert(0, self.osc_writer.host)
            self.port_entry.insert(0, self.osc_writer.port)

    #     self.update()
    #
    # def update(self):
    #     timeValue = str(self.json_reader.getTime())
    #     self.time_value_label.configure(text=timeValue)
    #     self.parent.after(1, self.update) # schedule next update (tkinter doesn't seem to provide a nice way to do every-iteration-updates)

    def destroy(self):
        self.frame.grid_forget()

    def onConnect(self):
        self.osc_writer.configure(host=self.host_entry.get(), port=self.port_entry.get())
