from mocap_bridge.utils.color_terminal import ColorTerminal

from mocap_bridge.interface.manager import Manager
from mocap_bridge.readers.json_reader import JsonReader
from mocap_bridge.writers.osc_writer import OscWriter

class RecordingPlayer:
    def __init__(self, json_file='../data/sampleRecording2.json', osc_host='127.0.0.1', osc_port=8080, manager=None, autoStart=False):
        # config
        self.json_file = json_file
        self.osc_host = osc_host
        self.osc_port = osc_port
        self.manager = manager
        self.reader = None
        self.writer = None

        if autoStart:
            self.start()

    def setup(self):
        # clean existing mess before we start creating a mess
        self.destroy()
        # let's make a mess
        if self.manager == None:
            self.manager = Manager()
        self.writer = OscWriter(host=self.osc_host, port=self.osc_port, manager=self.manager)
        self.reader = JsonReader(self.json_file, manager=self.manager)

    def destroy(self):
        if self.reader:
            self.reader.stop()
            self.reader = None
        if self.writer:
            self.writer.stop()
            self.writer = None
        if self.manager:
            self.manager = None

    def update(self):
        if self.reader:
            self.reader.update()

    def start(self):
        self.setup()

    def stop(self):
        self.destroy()

    def status(self):
        if self.reader != None:
            return 'playing'
        return 'stopped'

import Tkinter

class RecordingPlayerView:
    def __init__(self, player=None):
        self.player = player
        if self.player == None:
            self.player = RecordingPlayer()
        self.setup()
        # self.tk.mainloop(self.update)

    def setup(self):
        # create gui-elements
        self.tk = Tkinter.Tk()
        self.tk.title('Play MoCap recording')
        # self.tk.geometry('1000x330')
        self.file_label = Tkinter.Label(self.tk, text="JSON File")
        self.file_input = Tkinter.Entry(self.tk, width=20)
        self.osc_host_label = Tkinter.Label(self.tk, text="OSC Host")
        self.osc_host_input = Tkinter.Entry(self.tk, width=20)
        self.osc_port_label = Tkinter.Label(self.tk, text="OSC Port")
        self.osc_port_input = Tkinter.Entry(self.tk, width=20, text='8080')
        self.button = Tkinter.Button(self.tk, text="Start", command = self.onButtonClicked)
        self.status_label = Tkinter.Label(self.tk, text="")
        # position gui-elements
        self.file_label.grid(column=0, row=0)
        self.file_input.grid(column=1, row=0)
        self.osc_host_label.grid(column=0, row=1)
        self.osc_host_input.grid(column=1, row=1)
        self.osc_port_label.grid(column=0, row=2)
        self.osc_port_input.grid(column=1, row=2)
        self.button.grid(column=0, row=3)
        self.status_label.grid(column=1, row=3)

        self.file_input.insert(0, self.player.json_file)
        self.osc_host_input.insert(0,self.player.osc_host)
        self.osc_port_input.insert(0,self.player.osc_port)

    def update(self):
        #self.file_input.insert(0, self.player.json_file)
        #self.osc_host_input.insert(0,self.player.osc_host)
        #self.osc_port_input.insert(0,self.player.osc_port)

        self.tk.update()
        if self.player.status() == 'playing':
            self.status_label.config(text=str(self.player.reader.getTime()))

    def onButtonClicked(self):
        print('btn clicked: ' + self.player.status())
        if self.player.status() == 'stopped':
            self.player.start()
            self.button.config(text='Stop')
            return
        if self.player.status() == 'playing':
            self.player.stop()
            self.button.config(text='Play')


if False: # all following is old code for inspiration
    import Tkinter
    from natnet_parser import NatNetParser
    from terminal_colors import bcolors
    from OSC_link import OSCLink

    class NatNetGUI(object):
        def __init__(self):
            self.buildWindow()
            self.natnet = None
            self.osc = None
            self.top.mainloop()

        def natnet_connect_button_handler(self):

            if self.natnet is not None and self.natnet.isConnected():
                self.natnet = None
                self.natnet_link.configure(bg="red")
                self.natnet_connect_button.configure(text="connect")
            else:
                if self.natnet_host_input.get() == "":
                    host = None
                else:
                    host = self.natnet_host_input.get()

                if self.natnet_multi_input.get() == "":
                    multicast = None
                else:
                    multicast = self.natnet_multicast_input.get()

                if self.natnet_port_input.get() == "":
                    port = None
                else:
                    port = self.natnet_port_input.get()

                try:
                    self.natnet = NatNetParser(host=host, multicast=multicast, port=port)
                    self.natnet.updated += self.update
                    self.natnet.connect()
                    self.natnet.start()
                    self.natnet_link.configure(bg="green")
                    self.natnet_connect_button.configure(text="disconnect")
                except:
                    print bcolors.FAIL + "Error while connecting to NatNet" + bcolors.ENDC
                    self.natnet = None
                    self.natnet_link.configure(bg="red")


        def osc_connect_button_handler(self):
            if self.osc is not None and self.osc.isConnected:
                self.osc.close()
                self.osc = None
                self.osc_link.configure(bg="red")
                self.osc_connect_button.configure(text="connect")
            else:
                if self.osc_host_input.get() == "":
                    host = None
                else:
                    host = self.osc_host_input.get()

                if self.osc_port_input.get() == "":
                    port = None
                else:
                    port = self.osc_port_input.get()

                try:
                    self.osc = OSCLink(host=host, port=port)
                    self.osc_link.configure(bg="green")
                    self.osc_connect_button.configure(text="disconnect")
                except:
                    print bcolors.FAIL + "Error connecting to OSC server" + bcolors.ENDC
                    self.osc = None
                    self.osc_link.configure(bg="red")

        def update(self):
            for rb in self.natnet.rigidbodies:
                if self.osc is not None:
                    self.osc.sendRigibodyAsJSON(rb)

        def buildWindow(self):
            self.top = Tkinter.Tk()
            self.top.title("NatNet to OSC Communication == by David Jonas")
            self.top.geometry('1000x330')

            self.natnet_block = Tkinter.Frame(self.top, padx=50, pady=50)

            self.natnet_label = Tkinter.Label(self.natnet_block, text="NatNet connection", font=("Helvetica", "16"), padx=20, pady=20)
            self.natnet_label.grid(column=0, row=0)

            self.natnet_host_input_panel = Tkinter.Frame(self.natnet_block)
            self.natnet_host_input_label = Tkinter.Label(self.natnet_host_input_panel, text="Host", width=20)
            self.natnet_host_input = Tkinter.Entry(self.natnet_host_input_panel, width=20)
            self.natnet_host_input.insert(0, "0.0.0.0")
            self.natnet_host_input_label.grid(column=0, row=0)
            self.natnet_host_input.grid(column=1, row=0)
            self.natnet_host_input_panel.grid(column=0, row=1)

            self.natnet_multi_input_panel = Tkinter.Frame(self.natnet_block)
            self.natnet_multi_input_label = Tkinter.Label(self.natnet_multi_input_panel, text="Multicast adress", width=20)
            self.natnet_multi_input = Tkinter.Entry(self.natnet_multi_input_panel, width=20)
            self.natnet_multi_input_label.grid(column=0, row=0)
            self.natnet_multi_input.grid(column=1, row=0)
            self.natnet_multi_input_panel.grid(column=0, row=2)

            self.natnet_port_input_panel = Tkinter.Frame(self.natnet_block)
            self.natnet_port_input_label = Tkinter.Label(self.natnet_port_input_panel, text="port", width=20)
            self.natnet_port_input = Tkinter.Entry(self.natnet_port_input_panel, width=20)
            self.natnet_port_input.insert(0,"1511")
            self.natnet_port_input_label.grid(column=0, row=0)
            self.natnet_port_input.grid(column=1, row=0)
            self.natnet_port_input_panel.grid(column=0, row=3)

            self.natnet_connect_block = Tkinter.Frame(self.natnet_block)
            self.natnet_connect_button = Tkinter.Button(self.natnet_connect_block, text="Connect", command = self.natnet_connect_button_handler)
            self.natnet_link = Tkinter.Canvas(self.natnet_connect_block, width=20, height=20, bg="red")
            self.natnet_connect_button.grid(column=0, row=0)
            self.natnet_link.grid(column=1, row=0)
            self.natnet_connect_block.grid(column=0, row=4)

            self.osc_block = Tkinter.Frame(self.top, padx=50, pady=50)

            self.osc_label = Tkinter.Label(self.osc_block, text="OSC connection", font=("Helvetica", "16"), padx=20, pady=20)
            self.osc_label.grid(column=0, row=0)

            self.osc_host_input_panel = Tkinter.Frame(self.osc_block)
            self.osc_host_input_label = Tkinter.Label(self.osc_host_input_panel, text="Host", width=20)
            self.osc_host_input = Tkinter.Entry(self.osc_host_input_panel, width=20)
            self.osc_host_input.insert(0, "127.0.0.1")
            self.osc_host_input_label.grid(column=0, row=0)
            self.osc_host_input.grid(column=1, row=0)
            self.osc_host_input_panel.grid(column=0, row=1)

            self.osc_port_input_panel = Tkinter.Frame(self.osc_block)
            self.osc_port_input_label = Tkinter.Label(self.osc_port_input_panel, text="port", width=20)
            self.osc_port_input = Tkinter.Entry(self.osc_port_input_panel, width=20)
            self.osc_port_input.insert(0,"8080")
            self.osc_port_input_label.grid(column=0, row=0)
            self.osc_port_input.grid(column=1, row=0)
            self.osc_port_input_panel.grid(column=0, row=3)

            self.osc_connect_block = Tkinter.Frame(self.osc_block)
            self.osc_connect_button = Tkinter.Button(self.osc_connect_block, text="Connect", command = self.osc_connect_button_handler)
            self.osc_link = Tkinter.Canvas(self.osc_connect_block, width=20, height=20, bg="red")
            self.osc_connect_button.grid(column=0, row=0)
            self.osc_link.grid(column=1, row=0)
            self.osc_connect_block.grid(column=0, row=4)

            self.natnet_block.grid(column=0, row=0)
            self.osc_block.grid(column=1, row=0)

    n = NatNetGUI()
