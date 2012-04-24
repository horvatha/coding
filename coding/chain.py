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
        if self.verbosity and outputs[0].message != outputs[-1].message:
            print("Differs from the original:")
            print(str(len(outputs[0].message))+":", end="") # puts the characters count at the start
            max = len(outputs[0].message)
            if (max > len(output.message)):
              max = len(output.message)
            for i in range(max):
              if outputs[0].message[i] == output.message[i]:
                print ('\033[92m'+outputs[0].message[i],end="") # right characters, green
              else:
                print ('\033[31m'+outputs[0].message[i],end="") # wrong characters, red
            print('\033[0m') # return to defaults

        return outputs



