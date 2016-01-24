class ColorTerminal(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self):
        pass

    def output(self, msg, prefix=None):
        if prefix:
            msg = prefix + msg + ColorTerminal.ENDC
        print(msg)

    def warn(self, msg):
        self.output(msg, ColorTerminal.WARNING)

    def fail(self, msg):
        self.output(msg, ColorTerminal.FAIL)

    def success(self, msg):
        self.output(msg, ColorTerminal.OKGREEN)
