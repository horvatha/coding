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

#class Test(unittest.TestCase):
#
#    def testLoad(self):
#        chain = coding.Chain()
#        source = coding.Source([.5, .25, .125, .125])
#        chain.append(source)
#        chain.run()
#        self.assertEqual(chain[0], chain[-1])
#
#    def testErrors(self):
#        self.assertRaises(AssertionError, coding.Source, [.5, .5, .25, .25])

if __name__ == "__main__":
    unittest.main()

