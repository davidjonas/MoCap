from terminal_colors import bcolors

class ColorTerminal(object):
    _instance = None

    def __init__(self):
        pass

    def output(self, msg, prefix=None):
        if prefix:
            msg = prefix + msg + bcolors.ENDC
        print(msg)

    def warn(self, msg):
        self.output(msg, bcolors.WARNING)

    def fail(self, msg):
        self.output(msg, bcolors.FAIL)

    def success(self, msg):
        self.output(msg, bcolors.OKGREEN)
