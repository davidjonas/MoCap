from mocap_bridge.writers.json_writer import JsonWriter

import Tkinter as tk

class JsonWriterView:
    def __init__(self, json_writer=None, parent=None):
        self.writer = json_writer
        self.parent = parent
        self.recorded_files = []

        if self.writer == None:
            self.writer = JsonWriter()

        self.setup()

    def setup(self):
        # create gui-elements
        self.frame = tk.Frame(self.parent, padx=10, pady=10)
        self.frame.grid()

        # self.file_label = tk.Label(self.frame, text="JSON File: ")
        # self.file_entry = tk.Entry(self.frame, width=20)
        self.record_button = tk.Button(self.frame, text='Start recording', command=self.onRecordButton)
        self.status_label = tk.Label(self.frame, text='')
        self.log_label = tk.Label(self.frame, text='')

        # position elements
        # self.file_label.grid(column=0, row=0)
        # self.file_entry.grid(column=1, row=0)
        self.record_button.grid(column=0, row=0)
        self.status_label.grid(column=1, row=0)
        self.log_label.grid(column=0, row=1)

        # initialize
        if self.writer:
            # self.file_entry.insert(0, self.writer.path)
            self.updateStatus(self.writer)
            self.writer.startEvent += self.onStart
            self.writer.stopEvent += self.onStop
            self.writer.frameEvent += self.onFrame

    def destroy(self):
        if self.writer:
            self.writer.stop()
            self.writer = None

        self.frame.grid_forget()

    def onRecordButton(self):
        if self.writer.isRunning():
            self.writer.stop()
        else:
            self.writer.start()

    def onStart(self, json_writer):
        # self.writer.setPath(self.file_entry.get())
        self.recorded_files = list(set(self.recorded_files + [json_writer.path])) # list(set()) makes sure we only have unique values
        self.updateStatus(json_writer)

    def onStop(self, json_writer):
        # sets new default, timestamped target file for the next recording
        self.writer.setPath()
        self.updateStatus(json_writer)

    def onFrame(self, json_writer):
        self.updateStatus(json_writer)

    def updateStatus(self, json_writer):
        if json_writer.isRunning():
            self.record_button.configure(text='Stop recording')
            self.status_label.configure(text='Recorded '+str(json_writer.recordedFrames)+' frames')
        else:
            self.status_label.configure(text='Stopped')
            self.record_button.configure(text='Start recording')

        self.log_label.configure(text="\n".join(['Recorded files:']+self.recorded_files))
