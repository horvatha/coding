from coding.base import Bits, Message, Code, SYMBOLS, pprint
from random import random

class Source(object):
    """Creating radom messages."""
    def __init__(self, distribution, symbols=SYMBOLS):
        """Az objektum létrehozásakor az eloszlás helyességét ellenőrzi."""
        self.distribution = distribution
        assert len(distribution) <= len(symbols), "Túl kevés a jel."
        assert sum(distribution) == 1, "A valószínűségek összege nem 1, hanem %f." % sum(distribution)
        self.symbols = symbols
        self.n = len(distribution)

    def __str__(self):
        return pprint(self.distribution)

    def __repr__(self):
        return "Source({0})".format(self.distribution)

    def random_symbol(self, karakterkent=True):
        """Egy véletlen jelet ad vissza a megadott eloszlással."""
        rnd = random()
        summa = 0
        for i in range(len(self.distribution)):
            summa += self.distribution[i]
            if summa > rnd:
                break

        if karakterkent:
            return self.symbols[i]
        else:
            return i

    def message(self, n=100):
        """Egy véletlen üzenetet ad vissza a megadott eloszlással.

        Argumentumok:
            n: a jelek száma,
        """

        message = ""
        for i in range(n):
            symbol = self.random_symbol(karakterkent=False)
            message += self.symbols[symbol]
        return Message(message, self.symbols)

    uzenet = message

class FixSource(object):
    """Creating a constant message.

    >>> f = FixSource("ABCDD")
    >>> f.message()
    Message("5:ABCDD")
    >>> f = FixSource("0110", Bits)
    """

    def __init__(self, message, class_=Message):
        if isinstance(message, (Message, Bits)):
            self.__message = message
        else:
            assert class_ in [Message, Bits],\
                "class_ should be Message or Bits"
            assert isinstance(message, str)
            self.__message = class_(message)

    def message(self, n=100):
        return self.__message
