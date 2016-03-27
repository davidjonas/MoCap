from mocap_bridge.utils.color_terminal import ColorTerminal
from mocap_bridge.readers.json_reader import JsonReader
from mocap_bridge.utils.event import Event

import Tkinter
import tkFileDialog

class JsonReaderView:
    def __init__(self, json_reader, parent=None):
        self.json_reader = json_reader
        self.parent = parent
        self.setup()

    def setup(self):
        # create gui-elements
        self.frame = Tkinter.Frame(self.parent, padx=10, pady=10)
        self.frame.grid()

        self.file_text_label = Tkinter.Label(self.frame, text="JSON File")
        self.file_value_label = Tkinter.Label(self.frame, text=self.json_reader.path)
        self.time_text_label = Tkinter.Label(self.frame, text="time (s)")
        self.time_value_label = Tkinter.Label(self.frame, text="0")
        self.startstop_button = Tkinter.Button(self.frame, text='Stop', command=self.onStartStopButtonClicked)

        if not self.json_reader.isRunning:
            self.startstop_button.configure(text='Start')

        self.loadJsonButton = Tkinter.Button(self.frame, text='Load JSON File', command=self.onLoadJsonFileButton)

        # position elements
        self.file_text_label.grid(column=0, row=0)
        self.file_value_label.grid(column=1, row=0)
        self.time_text_label.grid(column=2, row=0)
        self.time_value_label.grid(column=3, row=0)
        self.startstop_button.grid(column=4, row=0)
        self.loadJsonButton.grid(column=5, row=0)

        if self.json_reader:
            self.json_reader.startEvent += self.onStart
            self.json_reader.stopEvent += self.onStop
            self.json_reader.updateEvent += self.onUpdate
            self.updateStatus(self.json_reader)

    def destroy(self):
        self.frame.grid_forget()

    def onStartStopButtonClicked(self):
        if self.json_reader.isRunning():
            self.json_reader.stop()
        else:
            self.json_reader.start()

    def onLoadJsonFileButton(self):
        file_path = tkFileDialog.askopenfile(**{})

        if file_path:
            self.json_reader.configure(path=file_path.name)
            self.json_reader.start()

    def onStart(self, json_reader):
        self.updateStatus(json_reader)

    def onStop(self, json_reader):
        self.updateStatus(json_reader)

    def updateStatus(self, json_reader):
        if json_reader.isRunning():
            self.startstop_button.configure(text='Stop')
            self.file_value_label.configure(text=json_reader.path)
        else:
            self.startstop_button.configure(text='Start')

    def onUpdate(self, json_reader):
        timeValue = str(json_reader.getTime())
        self.time_value_label.configure(text=timeValue)
