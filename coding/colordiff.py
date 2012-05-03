from coding import base
green = '\033[92m'
red = '\033[31m'
reset = '\033[0m'
def Diff(message1, message2):
  if (type(message1) is base.Message or type(message1) is base.Bits):
    text1 = message1.message
  else:
    text1 = message1
  if (type(message2) is base.Message or type(message2) is base.Bits):
    text2 = message2.message
  else:
    text2 = message2
  max = len(text1) if len(text1)>len(text2) else len(text2)
  for i in range(max):
    try:
      if text1[i] == text2[i]:
        print (green + text2[i], end = "")
      else:
        print (red   + text2[i], end = "")
    except IndexError:
      pass
  print (reset)
  return max
