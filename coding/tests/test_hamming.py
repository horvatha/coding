#!/usr/bin/env python3

"""Unittest for correction.Hamming"""

from coding import correction
from coding import source
from coding import base
import unittest
import random

UNCODED = "00101100"
CODED = "01010100111100"
BIT_SEQUENCES = (
    "011011010110",
    "000000000000",
    "111111111111",
    "1111111111",
    "0000000000",
    "0000011111",
    "0101010101",
    "1010101010",
    "11111111",
    "00000000",
    "00011111",
    "01010101",
    "10101010",
    "0110110000011101111011011101111000101111"
)
print("\n".join([str((bits, len(bits))) for bits in BIT_SEQUENCES]))


class TestCodeDecodeParts(unittest.TestCase):

    known_values = {
        4: (
            (UNCODED[:4], CODED[:7]),
            (UNCODED[4:], CODED[7:]),
            ("1", "111"),
            ("0110", "1100110"),
            ("110011", "1011100011"),
        ),
        10: (
            ("0100101110", "01011000101110"),
        ),
    }
    hamming = correction.Hamming(4)
    hamming10 = correction.Hamming(10)

    def test_part_coder(self):
        "hamming.part_coder should return the proper result"
        for length in self.known_values:
            hamming = correction.Hamming(length)
            for original, coded in self.known_values[length]:
                self.assertEqual(
                    hamming.part_coder(base.Bits(original)),
                    coded
                )

    def test_part_decoder(self):
        "hamming.part_decoder should return the proper result"
        for length in self.known_values:
            hamming = correction.Hamming(length)
            for original, coded in self.known_values[length]:
                self.assertEqual(
                    hamming.part_decoder(coded),
                    original
                )


class TestSingleErrorCorrection(unittest.TestCase):
    maxmr = (
        (4, 3),
        (11, 4),
        (26, 5),
    )
    mr = (
        (4, 3),
        (5, 4),
        (10, 4),
        )

    def test_message_bits(self):
        "SingleErrorCorrection.message_bits should give proper result."
        for m, r in self.maxmr:
            self.assertEqual(
                correction.SingleErrorCorrection.message_bits(r), m)

    def test_all_bits(self):
        "SingleErrorCorrection.all_bits should give proper result."
        for m, r in self.mr:
            self.assertEqual(correction.SingleErrorCorrection.all_bits(m), m+r)

    def test_redundant_bits(self):
        "SingleErrorCorrection.redundant_bits should give proper result."
        for m, r in self.mr:
            self.assertEqual(
                correction.SingleErrorCorrection.redundant_bits(m), r)

    def test_calculates_number_of_message_bits_from_all_bits(self):
        SEC = correction.SingleErrorCorrection
        for m in range(1, 30):
            self.assertEqual(SEC.message_bits(n=SEC.all_bits(m)), m)

    def test_error_in_message_bits_from_all_bits(self):
        "The length of the Hamming code could not be a power of 2."
        SEC = correction.SingleErrorCorrection
        for k in range(1, 30):
            with self.assertRaises(AssertionError):
                SEC.message_bits_from_all_bits(2**k)


class TestHelpFunctions(unittest.TestCase):
    def test_delete_parity_bits(self):
        "delete_parity_bits should delete the 2-power bits"
        known_pairs = (
            ("110100010000000100", '0000000000000'),
            ("PP1P234P5678901P23", '1234567890123'),
            ("PP1P2", '12'),
            ("PP1", '1'),
            ("PP", ''),
            ("P", ''),
            ("", ''),
            (CODED[7:], UNCODED[4:]),
            ("111", "1"),
            ("1100110", "0110"),
            ("1011100011", "110011"),
            )
        for coded, plain in known_pairs:
            self.assertEqual(correction.delete_parity_bits(coded), plain)


class TestCoderDecoder(unittest.TestCase):

    known_values = {
        4: (
            (UNCODED, CODED),
            (UNCODED[:5], "0101010111"),
        ),
        5: (
            ('1011001100', '011001100'+'110011000'),
            ('1011001100' + '1', '011001100'+'110011000'+'111'),
        ),
        10: (
            ("0100101110", "01011000101110"),
            ("0100101110" "1", "01011000101110" "111"),
            ("0100101110"*2, "01011000101110"*2),
        ),
    }

    def test_coder(self):
        "hamming.coder should return the proper result"
        for length in self.known_values:
            hamming = correction.Hamming(length)
            for original, coded in self.known_values[length]:
                self.assertEqual(
                    hamming.coder(base.Bits(original)).message,
                    coded
                )

    def test_decoder(self):
        "hamming.decoder should return the proper result"
        for length in self.known_values:
            hamming = correction.Hamming(length)
            for original, coded in self.known_values[length]:
                self.assertEqual(
                    hamming.decoder(base.Bits(coded)).message,
                    original
                )

    def test_decoder_gets_back_the_original_value_for_random_bits(self):
        source_ = source.Source([.5, .5], symbols="01")
        for length in range(2, 17, 2):
            hamming = correction.Hamming(length)
            for i in range(10):
                random_msg = source_.message(length).message
                self.assertEqual(
                    hamming.decoder(
                        hamming.coder(base.Bits(random_msg))
                    ).message,
                    random_msg
                )

    def test_decoder_gets_back_the_original_value(self):
        for length in range(2, 17):
            hamming = correction.Hamming(length)
            for message in BIT_SEQUENCES:
                self.assertEqual(
                    hamming.decoder(
                        hamming.coder(base.Bits(message))
                    ).message,
                    message
                )

    def test_decoder_gets_back_the_original_value_when_1_errors(self):
        source_ = source.Source([.5, .5], symbols="01")
        for length in range(4, 17, 2):
            hamming = correction.Hamming(length-2)
            for i in range(10):
                random_msg = source_.message(length).message
                random_index = random.randint(0, length-1)
                coded = hamming.coder(base.Bits(random_msg))
                erroneus = coded.flip_bits([random_index])
                self.assertEqual(
                    hamming.decoder(erroneus).message,
                    random_msg
                )

    def test_inverse_more_block(self):
        "decoded should be equal to the original even in case of more blocks"
        source_ = source.Source([.5, .5], symbols="01")
        for length in range(2, 17, 2):
            for i in range(10):
                block_length = random.randint(1, length-1)
                hamming = correction.Hamming(block_length)
                random_msg = source_.message(length).message
                self.assertEqual(
                    hamming.decoder(
                        hamming.coder(base.Bits(random_msg))
                    ).message,
                    random_msg
                )

    def test_partcoder10(self):
        "part_code should work properly"
        block_length = 10
        blocks = 2
        hamming = correction.Hamming(block_length)
        source_ = source.BitSource(2)
        random_block = source_.message(block_length).message
        hamming_code = hamming.coder(random_block*2)
        self.assertEqual(len(hamming_code), blocks*14)
        self.assertEqual(
            hamming_code.message,
            hamming.coder(random_block).message*2
        )


class TestCoderDecoderFunction(unittest.TestCase):
    def test_coder_decoder(self):
        "coder and decoder should work properly"
        for mesg in (
                '01110111',
                '110111',
                '011001111',
                '011110010111',
                ):
            code = correction.hamming_coder(mesg)
            self.assertEqual(correction.hamming_decoder(code), mesg)

    def test_decoder_raise_error_for_2_power_lenth_codes(self):
        "hamming_decoder should raise error for 2-power-length codes"
        for code in (
                '01110111',
                '1101',
                '01',
                '0',
                ):
            self.assertRaises(AssertionError, correction.hamming_decoder, code)

    def test_decoder_returns_empty_string_with_more_than_1_errors(self):
        for code in (
                '01010',
                ):
            self.assertEqual(correction.hamming_decoder(code), '')

if __name__ == "__main__":
    unittest.main()
