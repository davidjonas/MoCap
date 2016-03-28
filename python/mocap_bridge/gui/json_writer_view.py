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
            # generate new default (timestamped) json filename
            self.writer.setPath() # self.file_entry.get())
            # start recording
            self.writer.start()

    def onStart(self, json_writer):
        # add the currently recording file to the list of recorded files
        self.recorded_files.append(json_writer.path)
        # update GUI log
        self.log_label.configure(text="\n".join(['Recorded files:']+self.recorded_files))
        # change text of start/stop button
        self.record_button.configure(text='Stop recording')
        # update status label
        self.updateStatus(json_writer)

    def onStop(self, json_writer):
        # add recorded frame count to the file log
        self.recorded_files[-1] += ' ('+str(self.writer.recordedFrames)+' frames)'
        # update GUI log
        self.log_label.configure(text="\n".join(['Recorded files:']+self.recorded_files))
        # change start/button text
        self.record_button.configure(text='Start recording')
        # update status label
        self.updateStatus(json_writer)

    def onFrame(self, json_writer):
        self.updateStatus(json_writer)

    def updateStatus(self, json_writer):
        if json_writer.isRunning():
            self.status_label.configure(text='Recorded '+str(json_writer.recordedFrames)+' frames')
        else:
            self.status_label.configure(text='Not recording')
