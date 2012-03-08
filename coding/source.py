from coding.base import Bits, Message, Code, SYMBOLS, pprint
from random import random

class Source(object):
    """Egy osztály, amelyből jelsorozatok és kódolt változatuk előállítása lehetséges"""

    def __init__(self, distribution):
        """Az objektum létrehozásakor az eloszlás helyességét ellenőrzi."""
        self.distribution = distribution
        assert len(distribution) <= len(SYMBOLS), "Túl kevés a jel."
        assert sum(distribution) == 1, "A valószínűségek összege nem 1, hanem %f." % sum(distribution)
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
            return SYMBOLS[i]
        else:
            return i

    def message(self, n=100):
        """Egy véletlen üzenetet ad vissza a megadott eloszlással.

        Argumentumok:
            n: a jelek száma,
        """

        symbols = ""
        for i in range(n):
            symbol = self.random_symbol(karakterkent=False)
            symbols += SYMBOLS[symbol]
        return Message(symbols)

    uzenet = message

