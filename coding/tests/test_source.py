#!/usr/bin/env python3

"""Unittest for analyzer.py."""

import coding
from coding.base import Bits, Message, Code
import unittest

class TestMessage(unittest.TestCase):
    good_values = zip("ABCD   AAAA   3:AAA".split(),
                      "4:ABCD 4:AAAA 3:AAA".split())
    bad_values = "ABvD ÁAAA 3:AAA:zzz 4:ABC".split()

    def testStrFormats(self):
        "The str values should be good"
        for mesg, str_ in self.good_values:
            message = Message(mesg)
            self.assertEqual("{0}".format(message), str_)

    def testBadMessages(self):
        "should raise Error in bad cases"
        for mesg in self.bad_values:
            self.assertRaises(AssertionError, coding.Message, mesg)

class TestCode(unittest.TestCase):
    codes = (
        ("00011011", "ABCD"),
        ("01101100", "BCDA"),
            )
    def testCoding(self):
        "coder should return the right code"
        code = Code("00 01 10 11")
        for coded, message in self.codes:
            self.assertEqual(coded, code.coder(message))

    def testDecoding(self):
        "decoder should return the right message"
        code = Code("00 01 10 11")
        for coded, message in self.codes:
            self.assertEqual(message, code.decoder(coded))

    def testUndecodable(self):
        "undecodable bits should raise error"
        code = Code("00 01 10 11")
        self.assertRaises(ValueError, code.decoder, "011")

    def testBadCodes(self):
        "bad codes should raise error"
        bad_codes = ("0 01", "01 2")
        for code in bad_codes:
            self.assertRaises(AssertionError, Code, code)

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

class Test(unittest.TestCase):

    def testLoad(self):
        chain = coding.Chain()
        source = coding.Source([.5, .25, .125, .125])
        chain.append(source)
        chain.run()
        self.assertEqual(chain[0], chain[-1])

    def testErrors(self):
        self.assertRaises(AssertionError, coding.Source, [.5, .5, .25, .25])

if __name__ == "__main__":
    unittest.main()

