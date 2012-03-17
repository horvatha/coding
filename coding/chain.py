from coding import base

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
        print(output)
        outputs.append(output)
        for codec in reversed(self.codecs):
            output = codec.decoder(output)
            if self.verbosity: print(codec.__repr__(), "decoder")
            print(output)
            outputs.append(output)

        return outputs



