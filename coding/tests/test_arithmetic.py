#!/usr/bin/env python3

"""Unittest for correction.Hamming"""

from coding import arithmetic
import unittest


class TestArithmeticCode(unittest.TestCase):

    known_values = {
        "AB": (
            {"A": (0, .5), "B": (.5, 1)},
            {"A": 1, "B": 1},
            [('A', 0.0, 0.5), ('AB', 0.25, 0.5)],
            (0.25 + 0.5)/2,

        ),
        "AAAB": (
            {"A": (0, .75), "B": (.75, 1)},
            {"A": 3, "B": 1},
            [
                ('A', 0.0, 0.75),
                ('AA', 0.0, 0.5625),
                ('AAA', 0.0, 0.421875),
                ('AAAB', 0.31640625, 0.421875)
            ],
            (0.31640625 + 0.421875)/2,
        ),
        "ALMA": (
            {'A': (0, 0.5), 'L': (0.5, 0.75), 'M': (0.75, 1.0)},
            {"A": 2, "L": 1, "M": 1},
            [
                ('A', 0.0, 0.5),
                ('AL', 0.25, 0.375),
                ('ALM', 0.34375, 0.375),
                ('ALMA', 0.34375, 0.359375)
            ],
            (0.34375 + 0.359375)/2,
        ),
        # "BŐRÖNDÖDÖN": (
        #     {
        #         "B": (0,   0.1),
        #         "D": (0.1, 0.3),
        #         "N": (0.3, 0.5),
        #         "Ö": (0.5, 0.8),
        #         "Ő": (0.8, 0.9),
        #         "R": (0.9, 1.0),
        #     },
        #     {"B": 1, "D": 2, "N": 2, "Ö": 3, "Ő": 1, "R": 1},
        #     [
        #         ('B', 0.0, 0.1),
        #         ('BŐ', 0.09, 0.09999999999999999),
        #         ('BŐR', 0.095, 0.09599999999999999),
        #         ('BŐRÖ', 0.09559999999999999, 0.09589999999999999),
        #         ('BŐRÖN', 0.09568999999999998, 0.09574999999999999),
        #         ('BŐRÖND', 0.09569599999999999, 0.09570799999999999),
        #         ('BŐRÖNDÖ', 0.09570319999999999, 0.09570679999999998),
        #         ('BŐRÖNDÖD', 0.09570356, 0.09570427999999999),
        #         ('BŐRÖNDÖDÖ', 0.09570399199999999, 0.09570420799999999),
        #         ('BŐRÖNDÖDÖN', 0.09570405679999999, 0.09570409999999999)
        #     ],
        #     0.09570407839999999,
        # ),
    }

    def test_get_intervals_returns_the_proper_values(self):
        for arg, values in self.known_values.items():
            expected_value = values[0]
            return_value = arithmetic.ArithmeticCode.get_intervals(arg)
            for symbol in expected_value:
                lower, upper = return_value[symbol]
                expected_lower, expected_upper = expected_value[symbol]
                self.assertAlmostEqual(lower, expected_lower)
                self.assertAlmostEqual(upper, expected_upper)

    def test_count_symbols_returns_the_proper_values(self):
        for arg, values in self.known_values.items():
            return_value = values[1]
            self.assertEqual(arithmetic.count_symbols(arg), return_value)

    def test_code_intervals_returns_the_proper_values(self):
        for arg, values in self.known_values.items():
            if len(values) > 2:
                return_value = values[2]
                code = arithmetic.ArithmeticCode(arg)
                self.assertEqual(
                    code.coder_intervals(arg),
                    return_value
                )

    def test_coder_returns_the_proper_values(self):
        for arg, values in self.known_values.items():
            if len(values) > 3:
                return_value = values[3]
                code = arithmetic.ArithmeticCode(arg)
                self.assertEqual(
                    code.coder(arg),
                    return_value
                )

    def test_decoder_returns_the_proper_values(self):
        for text, values in self.known_values.items():
            if len(values) > 3:
                code_value = values[3]
                length = len(text)
                code = arithmetic.ArithmeticCode(text)
                self.assertEqual(
                    code.decoder(code_value, length=length),
                    text,
                )

if __name__ == "__main__":
    unittest.main()
