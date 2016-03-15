from mocap_bridge.utils.color_terminal import ColorTerminal
from mocap_bridge.readers.json_reader import JsonReader
from mocap_bridge.utils.event import Event

import Tkinter

class JsonReaderView:
    def __init__(self, json_reader, tk=None, frame=None):
        self.json_reader = json_reader
        self.tk = tk
        self.private_tk = False
        self.frame = frame
        self.startEvent = Event()
        self.stopEvent = Event()
        self.setup()

    def setup(self):
        # # create and configure view container if we didn't get an existing container
        if self.tk == None and self.frame == None:
            self.tk = Tkinter.Tk()
            self.tk.title('Json Reader')
            self.private_tk = True
            # self.tk.geometry('1000x330')

        # create gui-elements
        if self.frame == None:
            self.frame = Tkinter.Frame(self.tk, padx=10, pady=10)
            self.frame.grid(column=0, row=0)

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

    def update(self):
        timeValue = str(self.json_reader.getTime())
        try:
            if self.tk and self.private_tk:
                self.tk.update()
            self.time_value_label.configure(text=timeValue)
        except:
            self.destroy()
            return False

    def destroy(self):
        self.tk = None

    def onStartStopButtonClicked(self):
        if self.json_reader.isRunning():
            self.stopEvent(self)
            self.json_reader.stop()
            self.startstop_button.configure(text='Start')
        else:
            self.startEvent(self)
            self.json_reader.start()
            self.startstop_button.configure(text='Stop')
