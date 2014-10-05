#!/usr/bin/env python3

"""Üzenetek generálása és kódolása különböző kódokkal.
"""

from fractions import Fraction
import coding

eloszlasok = [
    (Fraction(1, 4), Fraction(1, 4), Fraction(1, 4), Fraction(1, 4))
    (Fraction(1, 2), Fraction(1, 4), Fraction(1, 8), Fraction(1, 8)),
]

for eloszlas in eloszlasok:
    forras = coding.Source(eloszlas)
    print("Az eloszlas", forras)
    uz = forras.message()
    print("A véletlen üzenet\n", uz)
    print("A szimbólumok darabszáma", uz.count())
    kod = coding.Code("00 01 10 11")
    print()
    print("  Az 1. kód:", kod)
    bitek = kod.coder(uz)
    print("  Az 1. kóddal kódolt üzenet\n", bitek)
    print("  1-esek és 0-ások száma", bitek.count())
    # uz2 = kod.decoder(bitek)
    # print("A visszakódolt üzenet\n", uz2)
    print()
    kod2 = coding.Code("0 10 110 111")
    print("  A 2. kód:", kod2)
    bitek = kod2.coder(uz)
    print("  A 2. kóddal kódolt üzenet\n", bitek)
    print("  1-esek és 0-ások száma", bitek.count())
    print("\n"*2)
