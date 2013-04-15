#!/usr/bin/env python3

"""Example using the package.
"""

from __future__ import division
from __future__ import print_function

__author__ = 'Arpad Horvath'

from coding import (Chain, FixSource, Source, Code, Hamming, Channel)

source = FixSource("ALABAMA")

chain = Chain(
    source,
    Code("00 01 10 11", symbols=source.symbols),
    Hamming(4),
    Channel(1),
    #Channel([24,26]),  # with code 00 01 10 11 decode is broken
    #Channel(.1),
    verbosity = 1,
    )
result = chain.print_run()
