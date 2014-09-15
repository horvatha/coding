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
             (("AA", "A", "BBB"), ("AA", "B", "BBB"))),
            (("AAABBB", "AAAABB"),
             (("AAA", "B", "BB"), ("AAA", "B", "BB"))),
            (("AABB", "AAAB"),
             (("AA", "B", "B",), ("AA", "A", "B",))),
        ])
        print(*[key for key in known_values.keys()], sep='\n')
        for args, result in known_values.items():
            self.assertEqual(diff.diff(*args), result)


if __name__ == '__main__':
    unittest.main()
