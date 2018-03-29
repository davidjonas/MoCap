from mocap_bridge.utils.color_terminal import ColorTerminal
from mocap_bridge.readers.json_reader import JsonReader
from mocap_bridge.utils.event import Event

import sys
if sys.version_info[0] >= 3:
    import tkinter as tk
else:
    import Tkinter as tk
    import tkFileDialog


class JsonReaderView:
    def __init__(self, json_reader, parent=None):
        self.json_reader = json_reader
        self.parent = parent
        self.setup()

    def setup(self):
        # create gui-elements
        self.frame = tk.LabelFrame(self.parent, text='Playback', padx=10, pady=10)
        self.frame.grid()

        self.loadJsonButton = tk.Button(self.frame, text='Load other JSON File', command=self.onLoadJsonFileButton)
        self.file_label = tk.Label(self.frame, text=self.json_reader.path)
        self.startstop_button = tk.Button(self.frame, text='Play', command=self.onStartStopButtonClicked)
        self.time_label = tk.Label(self.frame, text="time: 0s")

        # position elements
        self.loadJsonButton.grid(column=0, row=0)
        self.file_label.grid(column=1, row=0)
        self.startstop_button.grid(column=2, row=0)
        self.time_label.grid(column=0, row=1, columnspan=3)

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
            self.file_label.configure(text=json_reader.path)
        else:
            self.startstop_button.configure(text='Play')

    def onUpdate(self, json_reader):
        timeValue = '%.2f' % json_reader.getTime()
        self.time_label.configure(text='time: '+timeValue+'s')
