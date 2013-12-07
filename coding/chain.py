from coding import base
from coding import colortools

CHAINCOLOR = "blue"

class Run:
    "outputs of the runs"

    def __init__(self, outputs, chain):
        self.outputs = outputs
        self.chain = chain

    def iter_pairs(self):
        for pair in self.outputs:
            yield pair

    def print(self, outformat="{direction} {length:2} \"{message}\" {brokenness}",
              upmark="Δ", downmark="∇",
              with_elements=True):
        pairs = self.iter_pairs()
        broken_string = colortools.colored("broken", "red")
        for element in self.chain.iter_elements():
            if with_elements:
                print(element)
            try:
                down, up = next(pairs)
            except StopIteration:
                break
            with_difflib = not isinstance(down, base.Bits)
            message_down, message_up = colortools.diff(down, up, with_difflib=with_difflib)
            down_dict = dict(direction=downmark, length=len(down), message=message_down,
                             brokenness=broken_string if down.broken else "")
            up_dict = dict(direction=upmark, length=len(up), message=message_up,
                             brokenness=broken_string if up.broken else "")
            print(outformat.format(**down_dict))
            print(outformat.format(**up_dict))

class Chain:
    """It simulates an information transmitting chain.
    """
    def __init__(self, *elements, **kwargs):
        self.source, *self.codecs, self.channel = self.elements = elements
        self.levels = len(self.codecs) + 1
        self.verbosity = kwargs.pop("verbosity", 0)
        self.broken_string = colortools.colored("broken", "red")
        self.elementcolor = kwargs.pop("elementcolor", "blue")
        self.runs = []
        if kwargs:
            for key in kwargs:
                print("There is no argument called '{0}'".format(key))

    def __str__(self):
        return ",\n    ".join(repr(elem) for elem in self.elements)

    def __repr__(self):
        return "Channel({0},\n    verbosity={1})".format(self, self.verbosity)

    def iter_elements(self):
        for elem in self.elements:
            yield colortools.colored(repr(elem), self.elementcolor)

    def run(self):
        outputs = [[0, 0] for i in range(self.levels)]
        direction = 0
        level = 0
        output = self.source.message()
        outputs[level][direction] = output
        for codec in self.codecs:
            level += 1
            output = codec.coder(output)
            outputs[level][direction] = output
        direction = 1
        output = self.channel.run(output)
        outputs[level][direction] = output
        for codec in reversed(self.codecs):
            level -= 1
            output = codec.decoder(output)
            outputs[level][direction] = output
        self.runs.append(Run(outputs, self))

    def print_run(self, n=-1, **kwargs):
        if not self.runs:
            self.run()
        run = self.runs[n]
        run.print(**kwargs)

    def print_all(self, **kwargs):
        for run in self.runs:
            run.print(**kwargs)
            print()

