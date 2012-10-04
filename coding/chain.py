from coding import base
from coding import colortools

CHAINCOLOR = "blue"

class Chain(object):
    """It simulates an information transmitting chain.
    """
    def __init__(self, *args, **kwargs):
        self.source, *self.codecs, self.channel = args
        self.verbosity = kwargs.get("verbosity", 0)

    def print_element(self, *args, color=CHAINCOLOR, **kwargs):
        colortools.cprint(*args, color=color, **kwargs)

    def run(self):
        outputs = []
        output = self.source.message()
        if self.verbosity: self.print_element(self.source.__repr__())
        print(output)
        outputs.append(output)
        for codec in self.codecs:
            output = codec.coder(output)
            if self.verbosity: self.print_element(codec.__repr__(), "coder")
            print(output)
            outputs.append(output)
        output = self.channel.run(output)
        if self.verbosity: self.print_element(self.channel.__repr__())
        print(colortools.diff(output,outputs[-1]))
        outputs.append(output)
        for codec in reversed(self.codecs):
            output = codec.decoder(output)
            if self.verbosity: self.print_element(codec.__repr__(), "decoder")
            print(output)
            outputs.append(output)
        if self.verbosity and outputs[0].message != outputs[-1].message:
            print("Differs from the original:")
            print(colortools.diff(outputs[-1], outputs[0]), "broken" if output.broken else "")

        return outputs



