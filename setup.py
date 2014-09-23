#!/usr/bin/env python3
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

if sys.version_info[0] < 3:
    print("This module requires Python >= 3.0")
    sys.exit(0)

description="""
Classes teaching information and coding theory.
"""

options = dict(
    name = 'pycoding',
    version = '0.1',
    description = 'Classes teaching information and coding theory',
    long_description = description,
    license = 'GNU General Public License (GPL)',

    author = 'Arpad Horvath',
    author_email = 'horvath.arpad.szfvar@gmail.com',
    url = 'http://github.com/horvatha/coding',

    #package_dir = {'igraph': 'igraph'},
    packages = ['coding' ],
    #scripts = ['scripts/igraph'],
    #test_suite = "igraph.test.suite",

    platforms = 'ALL',
    keywords = ['math', 'information theory'],
    classifiers = [
      'Development Status :: 2 - Pre-Alpha',
      'Intended Audience :: Education',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering :: Mathematics',
      'Topic :: Software Development :: Libraries :: Python Modules',
      'License :: OSI Approved :: BSD License',
    ]
)

setup(**options)
