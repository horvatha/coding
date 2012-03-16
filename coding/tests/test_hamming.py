#!/usr/bin/env python3

"""Unittest for correction.Hamming"""

from coding import correction
from coding import source
from coding import base
import unittest

UNCODED = "00101100"
CODED = "01010100111100"

class TestCodeDecodeParts(unittest.TestCase):

    known_pairs = (
            (UNCODED[:4], CODED[:7]),
            (UNCODED[4:], CODED[7:]),
            ("1", "111"),
            ("0110", "1100110"),
            ("110011", "1011100011"),
            )
    hamming = correction.Hamming(4)

    def test_part_coder(self):
        "hamming.part_coder should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming.part_coder(base.Bits(original)),
                    coded
                    )
    def test_part_decoder(self):
        "hamming.part_decoder should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming.part_decoder(coded),
                    original
                    )


class TestHelpFunctions(unittest.TestCase):
    def test_delete_parity_bits(self):
        "delete_parity_bits should delete the 2-power bits"
        known_pairs = (
            ("110100010000000100", '0000000000000'),
            ("PP1P234P5678901P23", '1234567890123'),
            ("PP1P2", '12'),
            ("PP1", '1'),
            ("PP", ''),
            ("P", ''),
            ("", ''),
            (CODED[7:], UNCODED[4:]),
            ("111", "1"),
            ("1100110", "0110"),
            ("1011100011", "110011"),
            )
        for coded, plain in known_pairs:
            self.assertEqual(correction.delete_parity_bits(coded), plain)

class TestCoderDecoder(unittest.TestCase):

    known_pairs = (
            (UNCODED, CODED),
            (UNCODED[:5], "0101010111"),
            )
    hamming = correction.Hamming(4)

    def test_coder(self):
        "hamming.coder should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming.coder(base.Bits(original)).message,
                    coded
                    )

    def test_decoder(self):
        "hamming.decoder should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming.decoder(base.Bits(coded)).message,
                    original
                    )

    def test_inverse(self):
        "decoder should be the inverse of coder"
        source_ = source.Source([.5,.5], symbols="01")
        for i in range(10):
            random_msg = source_.message().message
            self.assertEqual(
                    self.hamming.decoder(
                        self.hamming.coder(base.Bits(random_msg))
                        ).message,
                    random_msg
                    )


if __name__ == "__main__":
    unittest.main()

