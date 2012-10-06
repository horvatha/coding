from coding import base
import sys
import difflib

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

USE_COLOR = sys.platform.startswith("linux") and not any(mod.startswith("idlelib.") for mod in sys.modules)
if USE_COLOR:
    escape = lambda color: '\033[{0}m'.format(COLORS[color])
else:
    escape = lambda color: ''

GOOD = escape("lightgreen")
WRONG = escape("red")
RESET = '\033[0m' if USE_COLOR else ''

colored = lambda string, color: escape(color) + string + RESET

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

def diff(text1, text2, with_difflib=False, use_space=False):
    """Compare two strings, Bits or Messages, and colorize the first one.

       text1 and text2 parameters can be string, Message or Bits. It will
       colorize message1 with the appropriate colors (green: correct,
       red: wrong).

    """
    if isinstance(text1, (base.Message, base.Bits)):
        text1 = text1.message
    if isinstance(text2, (base.Message, base.Bits)):
        text2 = text2.message

    colored1, colored2 = "", ""
    if min(len(text1), len(text2)) == 0:
        return colored(text1, "red"), colored(text2, "red")
    if with_difflib:
        assert text1 and text1[-1] != "\n" and text2 and text2[-1] != "\n"
        text1 += "\n"
        text2 += "\n"

        diff = list(difflib.Differ().compare(text1, text2))[:-1]

        for char in diff:
            if char[0] == "+":
                colored1 += " "
                colored2 += WRONG + char[-1]
            elif char[0] == " ":
                colored1 += GOOD + char[-1]
                colored2 += GOOD + char[-1]
            elif char[0] == "-":
                colored1 += WRONG + char[-1]
                colored2 += " "

        colored1 += RESET
        colored2 += RESET

        if not use_space:
            colored1 = colored1.translate({32: None})
            colored2 = colored2.translate({32: None})
    else:
        minlen = min(len(text1), len(text2))
        for i in range(minlen):
            if text2[i] != text1[i]:
                colored1 += WRONG + text1[i]
                colored2 += WRONG + text2[i]
            else:
                colored1 += GOOD + text1[i]
                colored2 += GOOD + text2[i]
        colored1 += RESET
        colored2 += RESET
        colored1 += text1[minlen:]
        colored2 += text2[minlen:]

    return colored1, colored2

