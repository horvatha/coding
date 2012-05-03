class Colordiff(object):
  green = '\033[92m'
  red = '\033[31m'
  reset = '\033[0m'
  @staticmethod
  def Diff(text1, text2):
    max = len(text1) if len(text1)>len(text2) else len(text2)
    for i in range(max):
      try:
        if text1[i] == text2[i]:
          print (Colordiff.green + text2[i], end = "")
        else:
          print (Colordiff.red   + text2[i], end = "")
      except IndexError:
        pass
    print (Colordiff.reset)
    return max
