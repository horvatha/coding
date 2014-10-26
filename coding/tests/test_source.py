#!/usr/bin/env python3

"""Unittest for source.py."""

import unittest
import coding
from coding.base import log2
from fractions import Fraction


class TestSource(unittest.TestCase):

    def setUp(self):
        self.sources = {
            "iid5": coding.Source(5),
            "ird4": coding.Source([1/2, 1/4, 1/8, 1/8]),
            "ird5": coding.Source([1/2, 1/8, 1/8, 1/8, 1/8]),
            "ird5_2": coding.Source([.2, .5, .1, .1, .1]),
        }

    def test_bad_distribution(self):
        "bad distribution should raise error"
        bad_distributions = ([.5, .6], [.5, .4])
        for value in bad_distributions:
            self.assertRaises(AssertionError, coding.Source, value)

    def test_message_length(self):
        "this distribution should return a message with given length"
        source = coding.Source([.5, .25, .125, .125])
        self.assertTrue(str(source.message()).startswith("100:"))

    def testIIDSource(self):
        "integer argument should create IID source"
        source = coding.Source(5)
        self.assertEqual(source.distribution, [Fraction(1, 5)]*5)

    def test_entropy(self):
        "entropy method should return the proper values"
        self.assertEqual(self.sources["iid5"].entropy(), log2(5))
        self.assertEqual(self.sources["ird4"].entropy(), 1.75)
        self.assertEqual(self.sources["ird5"].entropy(), 2)
        self.assertAlmostEqual(self.sources["ird5_2"].entropy(),
                               1.9609640474436814)

    def test_efficiency(self):
        "efficiency method should return the proper values"
        self.assertEqual(self.sources["iid5"].efficiency(), 1)
        self.assertEqual(self.sources["ird4"].efficiency(), 1.75/log2(4))
        self.assertEqual(self.sources["ird5"].efficiency(), 2/log2(5))
        self.assertAlmostEqual(self.sources["ird5_2"].efficiency(),
                               1.9609640474436814/log2(5))

    def test_string_version(self):
        iid5 = self.sources["iid5"]
        self.assertEqual(str(iid5),
                         "A:1/5 B:1/5 C:1/5 D:1/5 E:1/5")

if __name__ == "__main__":
    unittest.main()
