from mocap_bridge.utils.color_terminal import ColorTerminal
from mocap_bridge.readers.json_reader import JsonReader
from mocap_bridge.utils.event import Event

import Tkinter

class JsonReaderView:
    def __init__(self, json_reader=None, parent=None):
        self.json_reader = json_reader
        self.parent = parent
        self.startEvent = Event()
        self.stopEvent = Event()
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

        # position elements

        self.file_text_label.grid(column=0, row=0)
        self.file_value_label.grid(column=1, row=0)
        self.time_text_label.grid(column=0, row=1)
        self.time_value_label.grid(column=1, row=1)
        self.startstop_button.grid(column=0, row=2)

        self.update()

    def update(self):
        timeValue = str(self.json_reader.getTime())
        self.time_value_label.configure(text=timeValue)
        self.parent.after(1, self.update) # schedule next update (tkinter doesn't seem to provide a nice way to do every-iteration-updates)

    def onStartStopButtonClicked(self):
        if self.json_reader.isRunning():
            self.stopEvent(self)
            self.json_reader.stop()
            self.startstop_button.configure(text='Start')
        else:
            self.startEvent(self)
            self.json_reader.start()
            self.startstop_button.configure(text='Stop')
