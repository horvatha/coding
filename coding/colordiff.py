from coding import base
green = '\033[92m'
red = '\033[31m'
reset = '\033[0m'
def Diff(message1, message2):
  """Usage: import:
     from coding import colordiff
     Then use it colordiff.Diff(text1, text2)
     text1,text2 parameters can be string, message or bits, otherwise it needs to be cast to string
     it will print the text1 with the correct markings(green means correct, red means wrong)."""
  return_text = ""
  if (type(message1) is base.Message or type(message1) is base.Bits):  # convert to string
    text1 = message1.message
  else:
    text1 = message1
  if (type(message2) is base.Message or type(message2) is base.Bits): # convert to string
    text2 = message2.message
  else:
    text2 = message2

  max = len(text1) if len(text1)>len(text2) else len(text2) # check, which string is the longest

  for i in range(max):
    try:
      if text1[i] == text2[i]:
        return_text += green + text1[i]  # green characters are marked with green
      else:
        return_text += red   + text1[i]  # wrong characters are marked with red
    except IndexError: # catch index error, so it wont stop the program
      pass
  return_text += reset # reset the terminal, required to dismiss the effect green/red color on text
  return "{0}:{1}".format(max, return_text) # return with the specified format

