#!/usr/bin/env python3

"""Example using the package.
"""

from __future__ import division
from __future__ import print_function

__author__ = 'Arpad Horvath'

from coding import (Chain, FixSource, Source, Code, Hamming, Channel)

source = Source([.5, .25, .125, .125], length=10)

chain = Chain(
    source,
    Code("00 01 10 11", symbols=source.symbols),
    Hamming(4),
    Channel("4"),
    verbosity = 0,
    )
result = chain.run()
