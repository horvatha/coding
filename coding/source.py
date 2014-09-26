from coding.base import Bits, Message, Code, SYMBOLS, pprint, log2
from random import random

class CodingSourceError(Exception): pass

class Source:
    """Creating radom messages."""
    def __init__(self, distribution, *, symbols=SYMBOLS,
            **kwargs):
        """Create a Source object, and checks the validity of the distribution.

        Arguments:

        distribution: list or int
            The list of the probablities of the symbols or the number of
            symbols of an IID Source.
        symbols: default the uppercase letters in alphabetic order
            The symbols of the source. The first letter will have the first
            possibilities of the distribution variable and so on.

        Keyword arguments:

        length: int
            The default lenth of the message
        sum_precision: float, default 1e-13
            The precision of the sum of the probablities must be be 1.
        class_: Bits of Message
            The class of the source.
        """
        if isinstance(distribution, int):
            distribution = [1/distribution] * distribution
        self.distribution = distribution
        assert len(distribution) <= len(symbols), "Túl kevés a jel."
        self.class_ = kwargs.pop("class_", Message)
        if self.class_ is Bits:
            symbols = "01"
            assert len(self.distribution) < 3, 'distribution of Bits must be smaller than 3'
        else:
            assert self.class_ is Message, 'class_ must be Bits or Message'
        sum_precision = kwargs.pop("sum_precision", 1e-13)
        assert abs(sum(distribution) - 1) < sum_precision, "A valószínűségek összege nem 1, hanem %f." % sum(distribution)
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
        return pprint(self.distribution, self.symbols)

    def __repr__(self):
        msg = ", class_=Bits" if self.class_ is Bits else ""
        return "Source({0}{1})".format(self.distribution, msg)

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
        return self.class_(message, self.symbols)

    def entropy(self):
        return sum([p*log2(1/p) for p in self.distribution])

    def information(self):
        return [(sym, log2(1/p)) for sym, p in zip(self.symbols, self.distribution)]

    uzenet = message


class BitSource(Source):
    def __init__(self, distribution=2, **kwargs):
        super().__init__(distribution, symbols='01',
                class_=Bits, **kwargs)

class FixSource:
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

