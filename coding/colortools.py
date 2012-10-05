from coding import base
import sys

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

escape = lambda color: '\033[{0}m'.format(COLORS[color])

USE_COLOR = sys.platform.startswith("linux")

if USE_COLOR:
    GOOD = escape("lightgreen")
    WRONG = escape("red")
    RESET = '\033[0m'
else:
    GOOD = WRONG = RESET = ''

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
        args = list(args)
        print(color, end="")
    print(*args, **kwargs)
    if USE_COLOR:
        print(RESET, end="")

def diff(message1, message2):
  """Usage: import:
     from coding import colordiff
     Then use it colordiff.diff(text1, text2)
     text1, text2 parameters can be string, message or bits, otherwise it needs to be cast to string
     it will print the text1 with the correct markings(green means correct, red means wrong)."""
  return_text = ""
  if isinstance(message1, (base.Message, base.Bits)):  # convert to string
    text1 = message1.message
  else:
    text1 = message1
  if isinstance(message2, (base.Message, base.Bits)):  # convert to string
    text2 = message2.message
  else:
    text2 = message2

  lengths = [len(text) for text in (text1, text2)]
  for i in range(min(lengths)):
      if text1[i] == text2[i]:
          return_text += GOOD + text1[i]   # good characters are marked with green
      else:
          return_text += WRONG + text1[i]  # wrong characters are marked with red
  return_text += RESET # reset the terminal, required to dismiss the effect green/red color on text
  return_text += text1[min(lengths):lengths[0]]
  return "{0}:{1}".format(lengths[0], return_text)

