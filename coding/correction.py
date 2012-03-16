#!/usr/bin/env python3

"""Hamming coding

"""

from __future__ import division
from __future__ import print_function
from coding import base
from math import ceil

__author__ = 'Arpad Horvath'

class SingleErrorCorrection(object):
    @classmethod
    def message_bits(klass, r):
        return ceil(2**r - r - 1)
    @classmethod
    def redundant_bits(klass, m):
        assert isinstance(m, int) and m > 0
        r = 2
        while klass.message_bits(r) < m:
            r += 1
        return r
    @classmethod
    def all_bits(klass, r=None, m=None):
        if m:
            assert r is None, "If m is given, r must be None."
            r = klass.redundant_bits(m)
        return ceil(2**r - 1)

def delete_parity_bits(code):
    "Deletes parity bits from Hamming code"
    n = len(code)
    parity_bits = []
    parity = 1
    while parity <= n:
        parity_bits.append(parity)
        parity *= 2
    return "".join([code[i] for i in range(n) if i+1 not in parity_bits])

class Hamming(object):
    """Hamming code
    """
    def __init__(self, m=4):
        self.m = m
        self.n = SingleErrorCorrection.all_bits(m=m)

    def part_coder(self, bits, strong=False):
        """Codes the m-bits-long parts of the message.
        >>> hamming = Hamming(4)
        >>> hamming.part_coder("0110")
        '1100110'
        """
        if isinstance(bits, base.Bits):
            bits = bits.message
        else:
            assert isinstance(bits, str)
        if strong:
            assert len(bits) == self.m
        i = 1
        two_powers = [2**j for j in range(len(bits)+1)]
        hamming_code = []
        while bits:
            if i in two_powers:
                hamming_code.append(None)
            else:
                hamming_code.append(bits[0])
                bits = bits[1:]
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
        parts = bits.split(self.m)
        coded = [self.part_coder(part)
                 for part in parts]
        return base.Bits("".join(coded))

    def decoder(self, bits):
        if isinstance(bits, str):
            bits = base.Bits(bits)
        coded_parts = bits.split(self.n)
        parts = [self.part_decoder(part)
                 for part in coded_parts]
        return base.Bits("".join(parts))

    def part_decoder(self, bits, strong=False):
        bad_parity_sum = 0
        parity = 1
        while parity <= len(bits):
            summa = 0
            for i in range(len(bits)):
                if i+1 & parity and bits[i] == "1":
                    summa += 1
            if summa % 2:
                bad_parity_sum += parity
            parity *= 2
        if bad_parity_sum:
            if bad_parity_sum > self.n:
                raise base.UndecodeableError("bad_parity_sum={0} is greater then the code length={1}".format(bad_parity_sum, self.n))
            else:
                bits = base.change_bits(bits, bad_parity_sum)
        return delete_parity_bits(bits)

