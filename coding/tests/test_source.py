#!/usr/bin/env python3

"""Unittest for source.py."""

import unittest
import coding
from coding.base import log2

class TestSource(unittest.TestCase):

    def setUp(self):
        self.sources = {
                "iid5": coding.Source(5),
                "ird4": coding.Source([1/2, 1/4, 1/8, 1/8]),
                "ird5": coding.Source([1/2, 1/8, 1/8, 1/8, 1/8]),
            }

    def testBadDistribution(self):
        "bad distribution should raise error"
        bad_distributions = ([.5, .6], [.5, .4])
        for value in bad_distributions:
            self.assertRaises(AssertionError, coding.Source, value)

    def testMessageLength(self):
        "this distribution should return a message with given length"
        source = coding.Source([.5, .25, .125, .125])
        self.assertTrue(str(source.message()).startswith("100:"))

    def testIIDSource(self):
        "integer argument should create IID source"
        source = coding.Source(5)
        self.assertEqual(source.distribution, [1/5]*5)

    def testEntropy(self):
        "entropy method should return the proper values"
        self.assertEqual(self.sources["iid5"].entropy(), log2(5))
        self.assertEqual(self.sources["ird4"].entropy(), 1.75)
        self.assertEqual(self.sources["ird5"].entropy(), 2)

if __name__ == "__main__":
    unittest.main()

