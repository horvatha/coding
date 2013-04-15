from coding.base import Bits, Message, Code, SYMBOLS, pprint, log2
from random import random

class CodingSourceError(Exception): pass

class Source(object):
    """Creating radom messages."""
    def __init__(self, distribution, symbols=SYMBOLS,
            **kwargs):
        """Az objektum létrehozásakor az eloszlás helyességét ellenőrzi."""
        if isinstance(distribution, int):
            distribution = [1/distribution] * distribution
        self.distribution = distribution
        assert len(distribution) <= len(symbols), "Túl kevés a jel."
        assert sum(distribution) == 1, "A valószínűségek összege nem 1, hanem %f." % sum(distribution)
        self.symbols = symbols[:len(distribution)]
        self.n = len(distribution)
        self.length = kwargs.pop("length", None)
        if kwargs:
            raise CodingSourceError(
                "Invalid arument(s): {0}".format(
                    ", ".join(kwargs.keys())
                    )
                )

    def __str__(self):
        return pprint(self.distribution)

    def __repr__(self):
        return "Source({0})".format(self.distribution)

    def random_symbol(self, as_symbol=True):
        """Egy véletlen jelet ad vissza a megadott eloszlással."""
        rnd = random()
        summa = 0
        for i in range(len(self.distribution)):
            summa += self.distribution[i]
            if summa > rnd:
                break

        if as_symbol:
            return self.symbols[i]
        else:
            return i

    def message(self, n=None):
        """Egy véletlen üzenetet ad vissza a megadott eloszlással.

        Argumentumok:
            n: a jelek száma,
        """

        if n is None:
            n = self.length if self.length else 100
        message = ""
        for i in range(n):
            symbol = self.random_symbol(as_symbol=False)
            message += self.symbols[symbol]
        return Message(message, self.symbols)

    def entropy(self):
        return sum([p*log2(1/p) for p in self.distribution])

    def information(self):
        return [(sym, log2(1/p)) for sym, p in zip(self.symbols, self.distribution)]

    uzenet = message

class FixSource(object):
    """Creating a constant message.

    >>> f = FixSource("ABCDD")
    >>> f.message()
    Message("5:ABCDD")
    >>> f = FixSource("0110", class_=Bits)
    >>> f = FixSource("Baby", "AaBbYy")
    """

    def __init__(self, message, symbols=None, class_=Message,
            **kwargs):
        if symbols is None:
            self.symbols = "".join(sorted(list(set(message))))
        else:
            self.symbols = symbols
        if isinstance(message, (Message, Bits)):
            self.__message = message
        else:
            assert class_ in [Message, Bits],\
                "class_ should be Message or Bits"
            assert isinstance(message, str)
            self.__message = class_(message, symbols=self.symbols)

    def message(self):
        return self.__message

    def __repr__(self):
        return "FixSource({0!r})".format(self.__message.message)

