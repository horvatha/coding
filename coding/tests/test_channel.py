"""Tests of channel.py"""
import unittest
from coding import channel
import coding


class TestChannel(unittest.TestCase):
    """Test Channel module of channel.py"""

    bits = coding.Bits("01110010")

    known_values = (
        ((0, "num=0"), "0", "num", "hibamentes csatorna"),
        ((1, "num=1"), "1", "num", "csatorna 1 hibával"),
        (
            ("num=1-2", "num=1-2"),
            "1-2",
            "num",
            "csatorna 1 és 2 közötti hibával"
        ),
        (
            (.1, "ber=0.1"),
            "0.1",
            "ber",
            "csatorna, amely a bitek 0.1 részét elrontja"),
        (
            ([1, 3, -1], "bits=1,3,-1"),
            "1,3,-1",
            "bits",
            "csatorna, amely a következő biteket elrontja: 1,3,-1"
        )
    )

    def test_equivalent_desc_have_same_representations_and_run(self):
        for descriptions, value, type_, text in self.known_values:
            chan = channel.Channel(descriptions[0])
            for desc in descriptions:
                chan2 = channel.Channel(desc)
                chan.run(self.bits)
                self.assertEqual(repr(chan), repr(chan2))

    def test_desc_have_proper_values_and_types(self):
        for descriptions, value, type_, text in self.known_values:
            for desc in descriptions:
                chan = channel.Channel(desc)
                self.assertEqual(chan.value, value)
                self.assertEqual(chan.type, type_)

    def test_intervals(self):
        "should have the proper representation and should be run on input"
        for desc in ("1/7", "1-2", "1-2/7"):
            # TODO to complete
            chan = channel.Channel(desc)
            chan.run(self.bits)

    def test_verbose_description_returns_the_proper_value(self):
        for descriptions, value, type_, text in self.known_values:
            for desc in descriptions:
                this_channel = channel.Channel(desc)
                self.assertEqual(this_channel.verbose_description(), text)


def suite():
    channel_suite = unittest.makeSuite(TestChannel)
    return unittest.TestSuite([channel_suite])


def test():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == "__main__":
    test()
