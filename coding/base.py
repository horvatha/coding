"""The base classes for the coding module.
"""

import string

SYMBOLS = string.ascii_uppercase

def pprint(list_):
    """Pretty string format for lists with symbols"""
    n = len(list_)
    list_ = ["{p[0]}:{p[1]}".format(p=pair) for pair in zip(SYMBOLS[:n], list_)]
    return ", ".join(list_)

class Message(object):
    """Message
    """
    def __init__(self, message, symbols=SYMBOLS):
        self.symbols = symbols
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
        return 'Message("{0}")'.format(self)

    def count(self):
        counter = {}
        for symbol in self.message:
            if symbol in counter:
                counter[symbol] += 1
            else:
                counter[symbol] = 1
        return counter


class Bits(Message):

    def __init__(self, bits):
        super().__init__(bits, symbols="01")

    def __repr__(self):
        return 'Bits("{0}")'.format(self)

class Code(object):
    """Code class

    >>> code = Code("00 01 10 11")
    """
    def __init__(self, code):
        assert set(code).issubset(set("01 "))
        code = code.split()
        self.code = code
        code = list(zip(code, SYMBOLS))
        self.__decode = dict(code)  #code: symbol
        self.__code = dict([(x,y) for y,x in code])  #symbol: code

    def __str__(self):
        return pprint(self.code)

    def __repr__(self):
        return "Code('{0}')".format(" ".join(self.code))

    def __len__(self):
        return len(self.__decode)

    def coder(self, message):
        if not isinstance(message, Message):
            message = Message(message)
        encoded = [self.__code[symbol] for symbol in message.message]
        encoded = "".join(encoded)
        return Bits(encoded)

    def decoder(self, bits):
        if not isinstance(bits, Bits):
            bits = Bits(bits)
        message = []
        bits = bits.message[:]
        #TODO infinite cycle solved?
        while bits:
            changed = False
            for code in self.__decode:
                if bits.startswith(code):
                    bits = bits[len(code):]
                    message.append(self.__decode[code])
                    changed = True
                    break
            if not changed:
                raise ValueError("The rest of the code is not decodable")
                break
        message ="".join(message)
        return Message(message)

    kodol = coder
    dekodol = decoder

