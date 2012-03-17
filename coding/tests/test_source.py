#!/usr/bin/env python3

"""Unittest for source.py."""

import unittest
import coding

class TestSource(unittest.TestCase):
    def testBadDistribution(self):
        "bad distribution should raise error"
        bad_distributions = ([.5, .6], [.5, .4])
        for value in bad_distributions:
            self.assertRaises(AssertionError, coding.Source, value)

    def testMessageLength(self):
        "this distribution should return a message with given length"
        source = coding.Source([.5, .25, .125, .125])
        self.assertTrue(str(source.message()).startswith("100:"))

if __name__ == "__main__":
    unittest.main()

