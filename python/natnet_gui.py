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
