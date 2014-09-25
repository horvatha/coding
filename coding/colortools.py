from __future__ import print_function
from coding import base
import sys
import itertools
from coding import diff

COLORS = dict(
    list(zip([
        'grey',
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
        'white',
        'lightgreen',
    ],
        list(range(30, 38)) + [92]
    ))
)

USE_COLOR = sys.platform.startswith("linux") and \
    not any(mod.startswith("idlelib.") for mod in sys.modules)


def escape(color):
    return '\033[{0}m'.format(COLORS[color]) if USE_COLOR else ''

GOOD = escape("lightgreen")
WRONG = escape("red")
RESET = '\033[0m' if USE_COLOR else ''


def cprint(*args, **kwargs):
    """Prints with the color given as keyword argument color.

    Other parameters will be passed to the print function.
    If there is no color keyword argument, it will print with red.

    Example:

        >>> list(COLORS)
        ['blue',
         'grey',
         'yellow',
         'lightgreen',
         'green',
         'cyan',
         'magenta',
         'white',
         'red']

        >>> cprint("alma", 10, end="!\n", color="red")

    """
    color = escape(kwargs.pop("color", "red"))
    if USE_COLOR:
        print(color, end="")
    print(*args, **kwargs)
    if USE_COLOR:
        print(RESET, end="")


def colorize(text, color="red", reset_color=True):
    color_escape = escape(color)
    parts = [color_escape, text]
    if reset_color:
        parts.append(RESET)
    return "".join(parts)


def alternate_colorized_text(text_list, colors=("green", "red")):
    color_cycle = itertools.cycle(colors)
    return "".join([colorize(text, next(color_cycle)) for text in text_list])


def color_diff(text1, text2, with_difflib=True, use_space=False):
    """Compare two strings, Bits or Messages, and colorize the first one.

       text1 and text2 parameters can be string, Message or Bits. It will
       colorize message1 with the appropriate colors (green: correct,
       red: wrong).

    """
    if isinstance(text1, (base.Message, base.Bits)):
        text1 = text1.message
    if isinstance(text2, (base.Message, base.Bits)):
        text2 = text2.message

    diff_function = diff.diff if with_difflib else diff.bitdiff
    splitted_texts = diff_function(text1, text2)

    return [alternate_colorized_text(splitted) for splitted in splitted_texts]
