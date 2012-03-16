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
            ("0110", "1100110"),
            ("110011", "1011100011"),
            )
    hamming = hamming.Hamming(4)

    def test_code_part(self):
        "hamming.part_coder should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming.part_coder(base.Bits(original)),
                    coded
                    )
    def test_decode_part(self):
        "hamming.part_decoder should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming.part_decoder(base.Bits(coded)),
                    original
                    )


class TestCoderDecoder(unittest.TestCase):

    known_pairs = (
            (UNCODED, CODED),
            (UNCODED[:5], "0101010111"),
            )
    hamming_ = hamming.Hamming(4)

    def test_coder(self):
        "hamming.coder should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming_.coder(base.Bits(original)).message,
                    coded
                    )

    def test_decoder(self):
        "hamming.decoder should return the proper result"
        for original, coded in self.known_pairs:
            self.assertEqual(
                    self.hamming_.decoder(base.Bits(coded)).message,
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

