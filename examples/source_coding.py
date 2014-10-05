#!/usr/bin/env python3

"""Source coding example

You can change the code words, the propabilities of the
symbols, and the errors of the channel.

"""

from __future__ import division
from __future__ import print_function

__author__ = 'Arpad Horvath'

from coding import (Chain, FixSource, Source, Code, Hamming, Channel)
from fractions import Fraction as F

source = Source(4, length=10)
#source = Source([F(1, 2), F(1, 4), F(1, 8), F(1, 8)], length=10)
#source = FixSource("ALABAMA")

chain = Chain(
    source,
    Code("1000 0100 0010 0001", symbols=source.symbols),
    Channel(0),
    verbosity=0,
    )
result = chain.print_run()
