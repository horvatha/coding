#!/usr/bin/env python3

"""Hamming coding

"""

from __future__ import division
from __future__ import print_function
from coding import base

__author__ = 'Arpad Horvath'

class Hamming(object):
    """Hamming code
    """
    def __init__(self, n=4):
        self.n = n

    def part_coder(self, part, strong=False):
        """Codes the n-bits-long parts of the message.
        >>> hamming = Hamming(4)
        >>> hamming.part_coder("0110")
        '1100110'
        """
        if isinstance(part, base.Bits):
            part = part.message
        else:
            assert isinstance(part, str)
        if strong:
            assert len(part) == self.n
        i = 1
        two_powers = [2**j for j in range(len(part)+1)]
        hamming_code = []
        while part:
            if i in two_powers:
                hamming_code.append(None)
            else:
                hamming_code.append(part[0])
                part = part[1:]
            i += 1

        i = 0
        for tp in two_powers:
            if tp > len(hamming_code):
                break
            number_of_ones = 0
            for j in range(tp, len(hamming_code)):
                if j+1 & tp != 0 and hamming_code[j] == "1":
                    number_of_ones += 1
            parity_bit = 0 if number_of_ones % 2 == 0 else 1
            hamming_code[tp - 1] = str(parity_bit)

        return "".join(hamming_code)

    def coder(self, bits):
        if isinstance(bits, str):
            bits = base.Bits(bits)
        else:
            assert isinstance(bits, base.Bits)
        parts = bits.split(self.n)
        coded = [self.part_coder(part)
                 for part in parts]
        return base.Bits("".join(coded))

