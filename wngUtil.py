# Copyright 2025 Juergen Humt
# 
# This file is part of FreeCADwing.
# 
#
#     FreeCADwing, is free  software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by the 
#     Free Software Foundation, either version 3 of the License or any later 
#     version.
# 
#     FreeCADwing is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License along 
#     with FreeCADwing.  If not, see <http://www.gnu.org/licenses/>.
#
#     version v2.0.0
# 

from math import atan, degrees
import numpy as np
import scipy.optimize as sp
import FreeCAD as App



def clltRib(App, kEnd, dxMax=0, dtSpr=0):
  # dxMax  moves the end point of the spar towards the profile trailing edge
  # dtSpr  spar taper, the spar width at the tip is smaller than the root by dtSpr
  doc = App.ActiveDocument

  oF = open('/home/jhumt/Flight/FreeCad/monoWing/sclRib.lis','w')
  apcP = App.Console.PrintMessage
  objList = doc.Objects
  cList = []

  
  k=0;
  for obj in objList:
    if (obj.FullName.find('Common') > 0):
      cList.append(obj)
      outS = str(k) + '  ' + obj.FullName + '\n'
      oF.write(outS)
      k+=1

  k2D=0
  for obj in objList:
    if (obj.FullName.find('Clone2D') > 0) and (k2D < kEnd):
      cList.append(obj)
      outS = str(k2D) + '  ' + obj.FullName + '\n'
      oF.write(outS)
      k2D+=1


  scData = []
  
  sX = 'Common'
  s2 = 'Common0'
  
  hdrStr = "objNm                 parStgPnt      ribLen      xMx        fMx\n"
  oF.write(hdrStr)
  
  # the nose part of the profile is an amount of t [mm] 
  # smaller than the outer rib contour for the nose planking
  tLess = 0.5
  
  # the nose planking is on the upper and lower side
  # so 2*tLess have to be subtracted from the hight
  zMin = 1.0e3; zMax=-1;
  jzMin = -1; jzMax = -1;


  tLs2 = 2*tLess
  lEnd = len(cList)  # -1
  for j in range(lEnd):
    c5 = cList[j]
    objNm = c5.FullName
    apcP(str(j) + ' #  ' + objNm + '\n')

    c5ec = c5.Shape.Edges[0].Curve
    z5 = c5ec.EndPoint[2]
    if z5 < zMin:
      zMin = z5  
      cMin = c5ec
      jzMin = j
       
    if z5 > zMax:
      zMax = z5  
      cMax = c5ec
      jzMax = j


    nwItm=[]

  # below tFncX is used to find the parameter for the upper part of the curve
  # where the x value is the same as on the lower curve. i.e. the point vertically
  # above the one on the lower part of the rib curve
    jEx1 = -1
    if jEx1 > 0:
      x=0.4;
      
      vL_ = c5ec.value(x)
      xL = vL_[0]
      zL = vL_[1]
      
      a=0.51; b=1.0; tol=1.0e-5; 
      res = sp.minimize_scalar(tFncX, bracket=(a,b), args=(c5ec,vL_[0]), method='Golden')
      zU_ =c5ec.value(res.x)
      xU = zU_[0]
      zU = zU_[1]
      
      outStr=f'{j:3d} {objNm:s}   res.x-> {res.x:10.5e}\n'
      apcP(outStr)
      # oF.write(outStr)
    
      outStr=f'xU  - xL -> {xU:10.5e} - {xL:10.5e}\n'
      apcP(outStr)

    # below the parameter for the stagnation point of the profile is found
    aL=0.47; bL=0.53; dmy=0.0
    res = sp.minimize_scalar(fndMinParX, bracket=(aL,bL), args=(c5ec,dmy), method='Golden')  
    xLen = c5ec.value(float(0.0))[0]
    xStgPnt = res.x
    #  outStr=f'## xRet {res.x:10.5e}  fRet {str(res):s}\n' # {res.f:10.5e}\n'
    outStr=f'{objNm:23s}   parStagPnt  {res.x:10.5e}  xLen {xLen:10.3f}' # {res.f:10.5e}\n'
    outS2 = f'{j:3d} {objNm:23s}  {xStgPnt:12.4e} {xLen:10.3f}' # {res.f:10.5e}\n'
  #  apcP(outStr)
  #   oF.write(outStr)
  # hdrStr = "objNm       parStgPnt             xLen"
    nwItm.append(objNm);   nwItm.append(res.x);   nwItm.append(xLen)
    
  
  # bL below is calculated such that its parameter is slightly
  # past the stagnation point
    aL= 0.3; bL= 1.05*xStgPnt; dmy=0.0
    res = sp.minimize_scalar(tFncXZ, bracket=(aL,bL), args=(c5ec), method='Golden')
    u= res.x;  zdMx = -res.fun
    outStr= outStr + f'  xMx {u:12.6e}  fMx {-res.fun:10.5f}\n'
    outS2 = outS2 +  f'  {u:12.6e}  {zdMx:10.5f}'
    nwItm.append(u);  nwItm.append(zdMx); 
    # calculate the scale factor necessary so that the nose part of the profile
    # is an amount of t [mm] smaller than the outer rib contour
    zScFc = (zdMx - tLs2)/zdMx
    outS2 = outS2 + f'  {zScFc:12.8e}\n'
    nwItm.append(zScFc)
  
    scData.append(nwItm)
      
    apcP(outStr)
    oF.write(outS2)
  
  # xMin is the root rib, since it is the rib at zMin.
  # dxMax > 0 shifts the end point of the wing main
  # spar towards the trailing edge of the profile
  xMin = scData[jzMin][3]*scData[jzMin][2]
  xMax = (1.0 - scData[jzMax][3])*scData[jzMax][2] + dxMax

  # xMin is larger, since it is the root rib
  alf1=90.0 - degrees(atan((xMin-xMax)/(zMax-zMin)))
  alf2=90.0 - degrees(atan((xMin-(xMax+dtSpr))/(zMax-zMin)))

  outS= f'  jzMax={jzMax:4d}  vmax={scData[jzMax][3]:9.5f}  xmax={scData[jzMax][2]:5.2f}    jzMin={jzMin:4d}    vmin ={scData[jzMin][3]:9.5f} xmin={scData[jzMin][2]:5.2f}\n'
  apcP(outS)
  oF.write(outS)
  outS= f'  xMax={xMax:8.2f}   xMin={xMin:8.2f}    zMax={zMax:8.2f}   zMin={zMin:8.2f}    alf1={alf1:8.2f}°    alf1={alf2:8.2f}°\n'
  apcP(outS)
  oF.write(outS)
  oF.close()
  rDat = {'xMin':xMin, 'alf1':alf1, 'alf2':alf2, 'jzMin':jzMin, 'cMin':cMin, 'xMax':xMax, 'jzMax':jzMax, 'cMax':cMax}
  return scData, cList, rDat


def tFncX(pX, prm1=0, prm2=0, prm3=0):
# finds the point on the upper rib curve of the
# same x value as that on the lower i.e. two points
# on the rib curve connected by a vertical line.
# this is needed since that position can not be 
# calculated, as the stagnation point is not at
# par= 0.5. 
#  pX     value of parameter on upper rib curve 
#  prm1   the rib curve
#  prm2   x value on lower rib curve
  xR = abs(prm1.value(pX)[0] - prm2)
  return xR


def fndMinParX(x, prm1=0, prm2=0, prm3=0):
# finds the parameter along the rib curve
# where upper curve begins  
  vL = prm1.value(x)
  return abs(vL[1])


def fndMaxThk(wngCrv):
#  finds the point of maximum profile thickness
  aL=0.3; bL=0.49; dmy=0.0
  res = sp.minimize_scalar(tFncXZ, bracket=(aL,bL), args=(wngCrv,dmy), method='Golden')
  return [res.x, res.fun]
    

def tFncXZ(x, prm1=0, prm2=0, prm3=0):
  vL_ = prm1.value(x)
  xL = vL_[0]
  zL = vL_[1]
  
  a=0.51; b=1.0; tol=1.0e-5; 
  res = sp.minimize_scalar(tFncX, bracket=(a,b), args=(prm1,vL_[0]), method='Golden')
  vU_ =prm1.value(res.x)
  xU = vU_[0]
  zU = vU_[1]
  
  zRet = -abs(zU - zL);
  return zRet
