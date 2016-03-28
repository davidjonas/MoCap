from mocap_bridge.readers.osc_reader import OscReader

import Tkinter as tk

class OscReaderView:
    def __init__(self, osc_reader=None, parent=None):
        self.reader = osc_reader
        self.parent = parent

        if self.reader == None:
            self.reader = OscReader()

        self.setup()

    def setup(self):
        # create gui-elements
        self.frame = tk.LabelFrame(self.parent, text='Incoming OSC', padx=10, pady=10)
        self.frame.grid()

        self.host_label = tk.Label(self.frame, text="OSC Host")
        self.host_entry = tk.Entry(self.frame, width=10)
        self.port_label = tk.Label(self.frame, text="Port")
        self.port_entry = tk.Entry(self.frame, width=5)
        self.connect_button = tk.Button(self.frame, text='(re-)connect', command=self.onConnectButton)
        self.disconnect_button = tk.Button(self.frame, text='disconnect', command=self.onDisconnectButton)
        self.status_label = tk.Label(self.frame, text='')

        # position elements
        self.host_label.grid(column=0, row=0)
        self.host_entry.grid(column=1, row=0)
        self.port_label.grid(column=2, row=0)
        self.port_entry.grid(column=3, row=0)
        self.connect_button.grid(column=4, row=0)
        self.disconnect_button.grid(column=5, row=0)
        self.status_label.grid(column=0, row=1, columnspan=6)

        # initialize
        if self.reader:
            self.host_entry.insert(0, self.reader.host)
            self.port_entry.insert(0, self.reader.port)

            self.reader.connectEvent += self.onConnect
            self.reader.disconnectEvent += self.onDisconnect

            self.updateStatus(self.reader)

    def destroy(self):
        self.frame.grid_forget()

    def onConnectButton(self):
        self.reader.stop()
        self.reader.configure(host=self.host_entry.get(), port=self.port_entry.get())
        self.reader.start()

    def onDisconnectButton(self):
        self.reader.stop()

    def onConnect(self, reader):
        self.updateStatus(reader)

    def onDisconnect(self, reader):
        self.updateStatus(reader)

    def updateStatus(self, reader):
        if reader.connected == True:
            self.status_label.config(text='Connected to '+str(reader.host)+'@'+str(reader.port))
        else:
            self.status_label.config(text='Disconnected')
