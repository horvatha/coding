#!/usr/bin/env python3

"""Unittest for hamming.py."""

from coding import base
import unittest

class TestMessage(unittest.TestCase):

    good_messages = (
            ("ABCD", ),
            ("4:ABCD", ),
            ("1011", "01"),
            ("4:1011", "01"),
            )

    bad_messages = (
            ("ABaCD", ),
            ("5:ABCD", ),
            ("1011", ),
            ("10A1", "01"),
            )

    def test_good_messages(self):
        "Message should accept good messages"
        for good_message in self.good_messages:
            base.Message(* good_message)

    def test_bad_messages(self):
        "Message should deny bad messages"
        for bad_message in self.bad_messages:
            self.assertRaises(AssertionError, base.Message, *bad_message)


if __name__ == "__main__":
    unittest.main()

