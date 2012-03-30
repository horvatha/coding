#!/usr/bin/env python3

"""Source coding example

You can change the code words, the propabilities of the
symbols, and the errors of the channel.

"""

from __future__ import division
from __future__ import print_function

__author__ = 'Arpad Horvath'

from coding import (Chain, FixSource, Source, Code, Hamming, Channel)

source = Source([1/4, 1/4, 1/4, 1/4], length=10)
#source = Source([1/2, 1/4, 1/8, 1/8], length=10)

chain = Chain(
    source,
    Code("1000 0100 0010 0001", symbols=source.symbols),
    Channel(0),
    verbosity = 0,
    )
result = chain.run()
