"""The base classes for the coding module.
"""

import string
import collections

import math
log2 = lambda x: math.log(x)/math.log(2)

SYMBOLS = string.ascii_uppercase


class CodingError(Exception):
    "The base class of the Errors of coding package."
    pass


class UndecodeableError(CodingError):
    pass


def pprint(list_):
    """Pretty string format for lists with symbols"""
    n = len(list_)
    list_ = ["{p[0]}:{p[1]}".format(p=pair) for pair in zip(SYMBOLS[:n], list_)]
    return " ".join(list_)


def change_bits(bits, index_list):
    """Changes the given bits of bits.

    Parameters:
        bits: a string like "01101"
        index_list: integer or list of integers
            The indices of the bits we want to
            change. The smallest index is 1, not 0.

    Returns:
        The changed bits as a string.

    """
    other_bit = {"0": "1", "1": "0"}
    if isinstance(index_list, int):
        index_list = [index_list]
    for index in index_list:
        assert index <= len(bits), \
            "index = {0} must be smaller than len(bits) = {1}".format(
                index,
                len(bits)
            )
        bits = bits[:index-1] + other_bit[bits[index-1]] + bits[index:]
    return bits


class Message:
    """Message
    """
    def __init__(self, message, symbols=SYMBOLS, broken=False):
        self.symbols = symbols
        self.broken = broken
        parts = message.split(":")
        assert len(parts) < 3, "too many colons"
        if len(parts) == 2:
            message = parts[1]
            assert len(message) == int(parts[0]), "bad counter value"
        message = message if len(parts) == 1 else parts[1]
        assert set(message).issubset(set(self.symbols))
        self.__message = message

    @property
    def message(self):
        return self.__message

    @message.setter
    def message(self, message):
        assert set(message).issubset(set(self.symbols))
        self.__message = message

    def __str__(self):
        return "{0}:{1}".format(len(self.message), self.message)

    def __repr__(self):
        is_broken = ", broken=True" if self.broken else ""
        return 'Message("{0}"{1})'.format(self, is_broken)

    def __len__(self):
        return len(self.message)

    def count(self):
        counter = collections.OrderedDict()
        for symbol in self.symbols:
            counter[symbol] = 0
        for symbol in self.message:
            counter[symbol] += 1
        return list(counter.items())

    def split(self, n):
        """Splits the message into n-symbols-long parts"""
        divpoints = range(0, len(self.message), n)
        return [self.message[divpoints[i]:divpoints[i]+n]
                for i in range(len(divpoints))]


class Bits(Message):

    def __init__(self, bits, broken=False):
        super().__init__(bits, symbols="01", broken=broken)

    def __repr__(self):
        return 'Bits("{0}")'.format(self)

    def flip_bits(self, indices):
        bits = list(self.message)
        for i in indices:
            bits[i] = "0" if bits[i] == "1" else "1"
        return Bits("".join(bits))


class Code:
    """Code class

    >>> code = Code("00 01 10 11")
    """
    def __init__(self, code, **kwargs):
        assert set(code).issubset(set("01 ")),\
            "The code should have 0, 1 and --to divide codewords-- space"
        code = code.split()
        self.code = code
        assert len(code) == len(set(code)),\
            "There should not be duplicated codeword"
        for i in range(len(code)):
            for j in range(len(code)):
                if i != j:
                    assert not code[j].startswith(code[i]), \
                        "the code {0} should not start"\
                        " with the another codeword {1}".format(
                            code[j], code[i]
                        )
        self.symbols = kwargs.get("symbols", SYMBOLS)
        code = list(zip(code, self.symbols))
        self.__decode = dict(code)  # code: symbol
        self.__code = dict([(x, y) for y, x in code])  # symbol: code

    def __str__(self):
        return pprint(self.code)

    def __repr__(self):
        if self.symbols == SYMBOLS:
            return "Code('{0}')".format(" ".join(self.code))
        else:
            return "Code('{0}', symbols={1!r})".format(
                " ".join(self.code),
                self.symbols
            )

    def __len__(self):
        return len(self.__decode)

    def coder(self, message):
        if not isinstance(message, Message):
            message = Message(message)
        encoded = [self.__code[symbol] for symbol in message.message]
        encoded = "".join(encoded)
        return Bits(encoded)

    def decoder(self, bits, strict=False):
        if not isinstance(bits, Bits):
            bits = Bits(bits)
        message = []
        bits = bits.message[:]
        # TODO infinite cycle solved? I think, yes.
        broken = False
        while bits:
            changed = False
            for code in self.__decode:
                if bits.startswith(code):
                    bits = bits[len(code):]
                    message.append(self.__decode[code])
                    changed = True
                    break
            if not changed:
                broken = True
                if strict:
                    raise ValueError("The rest of the code is not decodable")
                break
        message = "".join(message)
        return Message(message, symbols=self.symbols, broken=broken)
