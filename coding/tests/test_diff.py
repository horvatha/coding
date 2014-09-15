from __future__ import print_function
import unittest
from coding import diff
from collections import OrderedDict


class TestDiff(unittest.TestCase):

    def test_diff_returns_proper_values(self):
        known_values = OrderedDict([
            (("AAABBB", "AAABBB"),
             (("AAABBB",), ("AAABBB",))),
            (("AABDD", "AACDD"),
             (("AA", "B", "DD"), ("AA", "C", "DD"))),
            (("XAABDD", "AACDD"),
             (("", "X", "AA", "B", "DD"), ("AA", "C", "DD"))),
            (("AAABBB", "AABBBB"),
             (("", "A", "AABBB"), ("AABBB", "B"))),
            (("AAABBB", "AAAABB"),
             (("AAABB", "B"), ("", "A", "AAABB"))),
            (("AABB", "AAAB"),
             (("AAB", "B"), ("", "A", "AAB"))),
        ])
        for args, result in known_values.items():
            self.assertEqual(diff.diff(*args), result)


class TestDiffBits(unittest.TestCase):

    def test_diffbits_returns_proper_values(self):
        known_values = OrderedDict([
            (
                ("010011", "010011"),
                (("010011",), ("010011",))
            ),
            (
                ("010011", "011011"),
                (("01", "0", "011",), ("01", "1", "011",))
            ),
            (
                ("110011", "010011"),
                (("", "1", "10011",), ("", "0", "10011",))
            ),
            (
                ("1100111", "0100110"),
                (("", "1", "10011", "1"), ("", "0", "10011", "0"))
            ),
            (
                ("110011", "0100110"),
                (("", "1", "10011"), ("", "0", "10011", "0"))
            ),
            (
                ("1100111", "010011"),
                (("", "1", "10011", "1"), ("", "0", "10011"))
            ),
        ])
        for args, result in known_values.items():
            self.assertEqual(diff.bitdiff(*args), result)


class TestSplitBits(unittest.TestCase):
    known_values = [
        # with bits of the same length
        (
            ([6], "010011", "010011"),
            (("010011",), ("010011",))
        ),
        (
            ([2, 3, 6], "010011", "011011"),
            (("01", "0", "011",), ("01", "1", "011",))
        ),
        (
            ([0, 1, 6], "110011", "010011"),
            (("", "1", "10011",), ("", "0", "10011",))
        ),
        (
            ([0, 1, 6, 7], "1100111", "0100110"),
            (("", "1", "10011", "1"), ("", "0", "10011", "0"))
        ),
        # with bits of different length
        (
            ([0, 1, 6], "110011", "0100110"),
            (("", "1", "10011"), ("", "0", "10011", "0"))
        ),
        (
            ([0, 1, 6], "0100110", "110011"),
            (("", "0", "10011", "0"), ("", "1", "10011"))
        ),
    ]

    def test_split_bits_returns_proper_values(self):
        for args, result in self.known_values:
            self.assertEqual(
                diff.split_bits(*args),
                result
            )
            reordered_args = args[0], args[2], args[1]
            reordered_result = (result[1], result[0])
            self.assertEqual(
                diff.split_bits(*reordered_args),
                reordered_result
            )

    def test_get_division_points_returns_proper_values(self):
        for args, result in self.known_values:
            division_points, bits0, bits1 = args
            self.assertEqual(
                diff.get_division_points(bits0, bits1),
                division_points
            )

    def test_split_one_bit_sequence_returns_proper_values(self):
        known_values = [
            (
                ([6], "010011"),
                ("010011",)
            ),
            (
                ([6], "010011"),
                ("010011",)
            ),
            (
                ([2, 3, 6], "011011"),
                ("01", "1", "011")
            ),
            (
                ([2, 3, 6], "010011"),
                ("01", "0", "011")
            ),
            (
                ([0, 1, 6], "110011"),
                ("", "1", "10011")
            ),
            (
                ([0, 1, 6], "010011"),
                ("", "0", "10011")
            ),
            (
                ([0, 1, 6], "010011"),
                ("", "0", "10011")
            ),
            (
                ([0, 1, 6, 7], "1100111"),
                ("", "1", "10011", "1")
            ),
            (
                ([0, 1, 6, 7], "0100110"),
                ("", "0", "10011", "0")
            ),
            (
                ([0, 1, 6, 7], "0100110"),
                ("", "0", "10011", "0")
            ),
            (
                ([0, 1, 6], "110011"),
                ("", "1", "10011")
            ),
        ]
        for args, result in known_values:
            division_points, bits = args
            self.assertEqual(
                diff.split_one_bit_sequence(*args),
                result
            )
            self.assertEqual(
                diff.split_one_bit_sequence(division_points[:-1], bits),
                result
            )


if __name__ == '__main__':
    unittest.main()
