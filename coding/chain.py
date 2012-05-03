from coding import base
from coding import colordiff

class Chain(object):
    """It simulates an information transmitting chain.
    """
    def __init__(self, *args, **kwargs):
        self.source, *self.codecs, self.channel = args
        self.verbosity = kwargs.get("verbosity", 0)

    def run(self):
        outputs = []
        output = self.source.message()
        if self.verbosity: print(self.source.__repr__())
        print(output)
        outputs.append(output)
        for codec in self.codecs:
            output = codec.coder(output)
            if self.verbosity: print(codec.__repr__(), "coder")
            print(output)
            outputs.append(output)
        output = self.channel.run(output)
        if self.verbosity: print(self.channel.__repr__())
        print(colordiff.Diff(output,outputs[-1]))
        outputs.append(output)
        for codec in reversed(self.codecs):
            output = codec.decoder(output)
            if self.verbosity: print(codec.__repr__(), "decoder")
            print(output)
            outputs.append(output)
        if self.verbosity and outputs[0].message != outputs[-1].message:
            print("Differs from the original:")
            print(colordiff.Diff(outputs[0],outputs[-1]))

        return outputs



