#!/usr/bin/env python3

"""Unittest for chain.py."""

from __future__ import print_function
import unittest
from coding import (Chain, FixSource, Code, Hamming, Channel, Message, Bits)


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


fix_source = FixSource("ALABAMA")
known_values = (
    (
        Chain(
            fix_source,
            Code("00 01 10 11", symbols=fix_source.symbols),
            Hamming(4),
            Channel("bits=3,11,17,21,21,24,26"),
            verbosity=1,
        ),
        [
            [Message("7:ALABAMA"), Message("6:ALABAM")],
            [Bits("14:00100001001100"), Bits("12:001000010011")],
            [
                Bits("26:01010101101001100001100000"),
                Bits("26:01110101100001101001100101")
            ]
        ],
        (
            FixSource('ALABAMA'),
            Code('00 01 10 11', symbols='ABLM'),
            Hamming(4),
            Channel("bits=3,11,17,21,21,24,26")
        ),

    ),
)


class TestRun(unittest.TestCase):
    def test_run_can_print(self):
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
        run = chain.runs[0]
        print(run.outputs, run.chain.elements, sep="\n")

    def test_runs_create_proper_attributes(self):
        for chain, outputs, elements in known_values:
            chain.run()
            run = chain.runs[0]
            self.assertEqual(repr(run.chain.elements), repr(elements))
            for output_pair, run_output_pair in zip(outputs, run.outputs):
                for i in (0, 1):
                    self.assertEqual(
                        output_pair[i].message,
                        run_output_pair[i].message
                    )

if __name__ == "__main__":
    unittest.main()
