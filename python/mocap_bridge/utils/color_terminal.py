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

    def red(self, msg): self.output(msg, ColorTerminal.FAIL)
    def yellow(self, msg): self.output(msg, ColorTerminal.WARNING)
    def blue(self, msg): self.output(msg, ColorTerminal.OKBLUE)
    def green(self, msg): self.output(msg, ColorTerminal.OKGREEN)
    def bold(self, msg): self.output(msg, ColorTerminal.BOLD)
    def underline(self, msg): self.output(msg, ColorTerminal.UNDERLINE)
    def header(self, msg): self.output(msg, ColorTerminal.HEADER)

    def warn(self, msg): self.yellow(msg)
    def fail(self, msg): self.red(msg)
    def success(self, msg): self.output(msg, ColorTerminal.OKGREEN)
