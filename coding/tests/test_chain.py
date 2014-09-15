#!/usr/bin/env python3

"""Unittest for chain.py."""

import unittest
from coding import (Chain, FixSource, Code, Hamming, Channel)


class TestChain(unittest.TestCase):

    def test_hamming_code_can_correct_1_error(self):
        'Hamming code could correct 1 error.'
        for block_length in range(4, 8):
            source = FixSource("ALABAMA")
            chain = Chain(
                source,
                Code("00 01 10 11", symbols=source.symbols),
                Hamming(block_length),
                Channel(1),
                verbosity=1,
            )
            chain.run()
            for level in [0, 1]:
                init, final = chain.runs[-1].outputs[level]
                self.assertEqual(init.message, final.message)

    def test_hamming_code_with_0_error(self):
        for block_length in range(10, 11):
            source = FixSource("BCDAABDBDCDBDBDCACDD")
            chain = Chain(
                source,
                Code("00 01 10 11", symbols="ABCD"),
                Hamming(block_length),
                Channel(0),
                verbosity=0,
            )
            chain.run()
            for level in [0, 1]:
                init, final = chain.runs[-1].outputs[level]
                self.assertEqual(init.message, final.message)


class TestRun(unittest.TestCase):
    def test_print(self):
        source = FixSource("ALABAMA")
        chain = Chain(
            source,
            Code("00 01 10 11", symbols=source.symbols),
            Hamming(4),
            Channel("bits=3,11,17,21,21,24,26"),
            verbosity=1,
        )
        chain.print_run()
        print()
        chain.print_run(with_elements=False)

if __name__ == "__main__":
    unittest.main()
