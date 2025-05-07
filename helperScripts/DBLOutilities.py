import sys

class PrintLogger:
    def __init__(self, filename, mode='a'):
        self.terminal = sys.__stdout__  # original stdout
        self.log = open(filename, mode)

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # Support flush for compatibility with some environments
        self.terminal.flush()
        self.log.flush()
