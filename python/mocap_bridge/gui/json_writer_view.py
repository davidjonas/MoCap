from mocap_bridge.writers.json_writer import JsonWriter

import Tkinter as tk

class JsonWriterView:
    def __init__(self, json_writer=None, parent=None):
        self.writer = json_writer
        self.parent = parent

        if self.writer == None:
            self.writer = JsonWriter()

        self.setup()

    def setup(self):
        # create gui-elements
        self.frame = tk.Frame(self.parent, padx=10, pady=10)
        self.frame.grid()

        self.file_label = tk.Label(self.frame, text="JSON File: <none>")
        self.record_button = tk.Button(self.frame, text='Start recording', command=self.onRecordButton)
        self.status_label = tk.Label(self.frame, text='')

        # position elements
        self.file_label.grid(column=0, row=0)
        self.record_button.grid(column=2, row=0)
        self.status_label.grid(column=3, row=0)

        # initialize
        if self.writer:
            self.updateStatus(self.writer)
            self.writer.startEvent += self.onStart
            self.writer.stopEvent += self.onStop

    def destroy(self):
        if self.writer:
            self.writer.stop()
            self.writer = None

        self.frame.grid_forget()

    def onRecordButton(self):
        if not self.writer: return

        if self.writer.isRunning():
            self.writer.stop()
            # sets new default, timestamped target file for the next recording
            self.writer.setDefaultPath()
        else:
            self.writer.start()

    def onStart(self, json_writer):
        self.updateStatus(json_writer)

    def onStop(self, json_writer):
        self.updateStatus(json_writer)

    def updateStatus(self, json_writer):
        if json_writer.isRunning():
            self.record_button.configure(text='Stop recording')
        else:
            self.record_button.configure(text='Start recording')

        if self.file_label:
            self.file_label.configure(text='JSON File: '+json_writer.path)
