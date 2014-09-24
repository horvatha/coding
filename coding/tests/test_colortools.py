#!/usr/bin/env python3
# coding: utf-8

"""Docstring"""
import unittest
import coding.colortools


class TestClass(unittest.TestCase):
    """TestGroup"""

    def setUp(self):
        """Setup Tests"""
        self.pairs = (
            ("ALBA", "ALIBABA"),
            ("ALBA", "ALBABA"),
            ("ALABAMA", "ALABALA"),
            ("ALABAMA", "ALABALAA"),
            ("ALABAMA", "ALABALAAA"),
            ("ALABAMA", "ALABALABA"),
            ("alma", "alfa"),
            ("alma", "almafa"),
            ("alma", "alfaj"),
            ("malac", "mallac"),
            ("alfaja", "alfaj"),
            ("malac", "maradsz"),
            ("malacod", "maradsz"),
            ("malacodat", "maradsz"),
            ("malacodat", ""),
            ("", ""),
        )

    def tearDown(self):
        """Tear down each test"""
        pass

    def test_color_diff_returns_proper_values(self):
        for first, second in self.pairs[:2]:
            print("'{}' <-> '{}' :".format(first, second))
            # print(*coding.colortools.color_diff(second, first))
            for colored in coding.colortools.color_diff(second, first):
                print(" "*10, colored)

    def test_color_diff_returns_proper_values_if_get_empty_string(self):
        for first, second in self.pairs[-2:]:
            print("'{}' <-> '{}' :".format(first, second))
            # print(*coding.colortools.color_diff(second, first))
            for colored in coding.colortools.color_diff(second, first):
                print(" "*10, colored)


def suite():
    Class_suite = unittest.makeSuite(TestClass)
    return unittest.TestSuite([Class_suite])


def test():
    runner = unittest.TextTestRunner()
    runner.run(suite())

if __name__ == "__main__":
    test()
