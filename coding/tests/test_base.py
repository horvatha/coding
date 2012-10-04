#!/usr/bin/env python3

"""Unittest for hamming.py."""

from coding import base
import unittest


class TestChangeBits(unittest.TestCase):
    known_pairs = (
        (("01110", 2),       "00110"),
        (("01110", [2]),     "00110"),
        (("01110", [1,2]),   "10110"),
        (("01110", [1,5]),   "11111"),
        )
    def test_results(self):
        for args, result in self.known_pairs:
            self.assertEqual(base.change_bits(*args), result)

class TestMessage(unittest.TestCase):

    good_messages = (
            ("ABCD", {"A":1, "B":1, "C":1, "D":1}),
            ("4:ABCD",  {"A":1, "B":1, "C":1, "D":1}),
            ("1011", "01", {"0":1, "1":3}),
            ("4:1011", "01", {"0":1, "1":3}),
            ("10A1", "01A", {"0":1, "1":2, "A":1}),
            ("10:ABABABABAB", {"A":5, "B":5}),
            )

    bad_messages = (
            ("ABaCD", ),
            ("5:ABCD", ),
            ("5:ABCD:A", ),
            ("1011", ),
            ("10A1", "01"),
            )

    def test_good_messages(self):
        "Message should accept good messages"
        for good_message in self.good_messages:
            base.Message(*good_message[:-1])

    def test_bad_messages(self):
        "Message should deny bad messages"
        for bad_message in self.bad_messages:
            self.assertRaises(AssertionError, base.Message, *bad_message)

    def test_split(self):
        "split should split in the proper way"
        message = base.Message("10:ABABABABAB")
        known_pairs = (
            (2, ["AB"]*5),
            (3, ["ABA", "BAB", "ABA", "B"]),
            (4, ["ABAB", "ABAB", "AB"]),
            (5, ["ABABA", "BABAB"]),
            (7, ["ABABABA", "BAB"]),
            (1, list("ABABABABAB")),
            )
        for n, list_ in known_pairs:
            self.assertEqual(message.split(n), list_)

    def test_count(self):
        "count should work in the proper way"
        for good_message in self.good_messages:
            message = base.Message(*good_message[:-1])
            self.assertEqual(message.count(),
                        good_message[-1]
                        )

    def testStringFormats(self):
        "should have the proper string format"
        str_formats = zip("ABCD   AAAA   3:AAA".split(),
                      "4:ABCD 4:AAAA 3:AAA".split())
        for mesg, str_ in str_formats:
            message = base.Message(mesg)
            self.assertEqual("{0}".format(message), str_)

class TestMessage(unittest.TestCase):
    def test_flip_bits(self):
        "Bits.flip_bits should flip the proper bits"
        bits = base.Bits("0111001")
        self.assertEqual(bits.flip_bits([0,4,5]).message,
                "1"*7)

    def test_count(self):
        "count should return the the symbols in the proper order"
        for msg_str in "CABBBAA BACCCA ABBBCCC CBA".split():
            mesg = base.Message(msg_str, symbols="ABC")
            self.assertEqual([x for x, y in mesg.count()], ["A", "B", "C"])

class TestCode(unittest.TestCase):
    codes = (
        ("00011011", "ABCD"),
        ("01101100", "BCDA"),
            )
    def testCoding(self):
        "coder should return the right code"
        code = base.Code("00 01 10 11")
        for coded, message in self.codes:
            self.assertEqual(coded, code.coder(message).message)

    def testDecoding(self):
        "decoder should return the right message"
        code = base.Code("00 01 10 11")
        for coded, message in self.codes:
            self.assertEqual(message, code.decoder(coded).message)

    def testUndecodable(self):
        "undecodable bits should raise error"
        code = base.Code("00 01 10 11")
        self.assertRaises(ValueError, code.decoder, "011")

    def testBadCodes(self):
        "bad codes should raise error"
        bad_codes = ("0 01", "01 2", "01 01")
        for code in bad_codes:
            self.assertRaises(AssertionError, base.Code, code)

if __name__ == "__main__":
    unittest.main()

