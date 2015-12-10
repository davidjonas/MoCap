import Tkinter
from natnet_parser import NatNetParser

class NatNetGUI(object):
    def __init__(self):
        self.buildWindow()
        self.natnet = None
        self.top.mainloop()

    def connect_button_handler(self):

        if self.natnet is not None and self.natnet.isConnected():
            self.natnet = None
            self.natnet_link.configure(bg="red")
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
                self.natnet_link.configure(bg="green")
                self.natnet_connect_button.configure(text="disconnect")
            except:
                self.natnet = None
                self.natnet_link.configure(bg="red")


    def buildWindow(self):
        self.top = Tkinter.Tk()
        self.top.title("NatNet to OSC Communication == by David Jonas")
        self.top.geometry('500x330')

        self.natnet_block = Tkinter.Frame(self.top, padx=50, pady=50)

        self.natnet_label = Tkinter.Label(self.natnet_block, text="NatNet connection", font=("Helvetica", "16"), padx=20, pady=20)
        self.natnet_label.grid(column=0, row=0)

        self.natnet_host_input_panel = Tkinter.Frame(self.natnet_block)
        self.natnet_host_input_label = Tkinter.Label(self.natnet_host_input_panel, text="Host", width=20)
        self.natnet_host_input = Tkinter.Entry(self.natnet_host_input_panel, width=20)
        self.natnet_host_input_label.grid(column=0, row=0)
        self.natnet_host_input.grid(column=1, row=0)
        self.natnet_host_input_panel.grid()

        self.natnet_multi_input_panel = Tkinter.Frame(self.natnet_block)
        self.natnet_multi_input_label = Tkinter.Label(self.natnet_multi_input_panel, text="Multicast adress", width=20)
        self.natnet_multi_input = Tkinter.Entry(self.natnet_multi_input_panel, width=20)
        self.natnet_multi_input_label.grid(column=0, row=0)
        self.natnet_multi_input.grid(column=1, row=0)
        self.natnet_multi_input_panel.grid()

        self.natnet_port_input_panel = Tkinter.Frame(self.natnet_block)
        self.natnet_port_input_label = Tkinter.Label(self.natnet_port_input_panel, text="port", width=20)
        self.natnet_port_input = Tkinter.Entry(self.natnet_port_input_panel, width=20)
        self.natnet_port_input_label.grid(column=0, row=0)
        self.natnet_port_input.grid(column=1, row=0)
        self.natnet_port_input_panel.grid()

        self.natnet_block.grid(column=0, row=0)

        self.natnet_connect_block = Tkinter.Frame(self.top)
        self.natnet_connect_button = Tkinter.Button(self.natnet_connect_block, text="Connect", command = self.connect_button_handler)
        self.natnet_link = Tkinter.Canvas(self.natnet_connect_block, width=20, height=20, bg="red")
        self.natnet_connect_button.grid(column=0, row=0)
        self.natnet_link.grid(column=1, row=0)
        self.natnet_connect_block.grid(column=0, row=1)

n = NatNetGUI()
