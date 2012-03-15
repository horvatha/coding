#!/usr/bin/env python3

"""Unittest for hamming.py."""

from coding import hamming
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
            )
    hamming = hamming.Hamming(4)

    def test_code_part(self):
        "hamming.code_part should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming.code_part(base.Bits(original)),
                    coded
                    )
    def test_decode_part(self):
        "hamming.decode_part should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming.decode_part(base.Bits(coded)),
                    original
                    )


class TestCodeDecode(unittest.TestCase):

    known_pairs = (
            (UNCODED, CODED),
            (UNCODED[:5], CODED[:10]),
            )
    hamming_ = hamming.Hamming(4)

    def test_code(self):
        "hamming.code should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming_.code(Bits(original)),
                    coded
                    )
    def test_decode(self):
        "hamming.decode should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming_.decode(Bits(coded)),
                    original
                    )
    def test_inverse(self):
        "decoder should be the inverse of coder"
        source_ = source.Source([.5,.5], symbols="01")
        for i in range(10):
            random_msg = source_.message()
            self.assertEqual(
                    self.hamming_.decoder(
                        self.hamming_.coder(random_msg)
                        ),
                    random_msg
                    )


if __name__ == "__main__":
    unittest.main()

