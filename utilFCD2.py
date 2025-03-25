import re


def splitStr(inpStr, spltChrs="[,;:]"):
  # split up string after ,;: and blank
  inpStr = inpStr.strip()

  # replace any of ,;: with a blank
  str1 = re.sub(spltChrs,' ',inpStr)
  # replace multiple blanks by just one
  str2 = " ".join(str1.split())
  return str2.split()


def splitPrStr(inpStr):
#split up string after [{(,;:)}] and blank
#
  inpStr=inpStr.strip()
#replace any of ,;: with a blank
  str1= re.sub('[{(,;:)}]',' ',inpStr)
#replace multiple blanks by just one
  str2= " ".join(str1.split())
  return str2.split()



def rdWngDat(flName, jB):
# jB =0 -> inner      jB =1 ->outer
  inF = open(flName,'r')
  
  wDat = []
  while True:
    inpLine = inF.readline()
    if not inpLine:
       break
    tk=splitStr(inpLine)
    wDat.append(float(tk[0]))

  if (jB > 0.5):
    kOfs= 4
    wDat[2] = wDat[3]  # inner end is tip of inner segment
    wDat[3] = wDat[1]  # outer end is wing span

    for k in range(4,8):
      wDat[k]=wDat[k+kOfs]

  wDat[8] = wDat[3] - wDat[2]
  inF.close()
  return wDat


def rdObjDat2(flName):
  print('reading ' + flName)
# jB =0 -> inner      jB =1 ->outer
  inF = open(flName,'r')

  wDat = []
  while True:
    inpLine = inF.readline()
    if not inpLine:
       break
    tk=splitStr(inpLine)
    if len(tk) > 2:
        wD = []
        wD.append(int(tk[2]))
        wD.append(int(tk[0]))
        wD.append(tk[1])
        wDat.append(wD)


  inF.close()
  wDatS = sorted(wDat) 

  return wDatS
