FreeCADwing is an open source software distributed under GPL v3. Read inside the files or read the GPL file which you find in the project.

FreeCADwing is a sequence of macros for FreeCAD that allow you to generate a tapered wing, the wing ribs and place the ribs in a drawing which you can export as an svg file to create e.g. the input for a laser cutter. You have to recolour the rib edges manually to red RGB = [255,0,0] for a laser cutter. The wing has an inner section, where the root profile is different from the outer profile of this section and an outer section which tapers towards the wing tip.

First define the wing geometry in file wDat19928.lis (the filename is, of course, arbitrary), it contains the data for both the inner and outer wing section. Line 0, the first line, is no longer used. Outer wing data start in line 8, after the first nRig.

First some remarks concerning different FreeCAD versions. Currently there seem to be two options:

a) To create the wing you have to run the macro mkRibAutoStrt9.FCMacro in freecad 18 because in higher versions, 19 through 21, the loft for the outer wing is not created, which in #18 works like a charm. This is quite annoying! Also all FreeCAD 18.x AppImages for me did not run in Debian 12 bookworm. My work around was to install the Windows version of FreeCAD 18.0 under wine. You can not work with the program, since the graphic window is blocked but you can run the mkRibAutoStrt9.FCMacro. The wing is generated all right. You can save the file, load it in e.g. FreeCAD 21 and proceed by runnig the other macros. 

b) use the latest FreeCAD development version. 
With the version 0.22.0dev I was able to run all the macros, although the version seems to crash now and then.  
OS: Debian GNU/Linux 12 (bookworm) (GNOME/gnome)
Word size of FreeCAD: 64-bit  
Version: 0.22.0dev.38553 (Git) AppImage  
Build type: Release 
Branch: main  
Hash: 59c1ccec3e6b70f56eeee8f94d361019b84bd850   
Python 3.11.9, Qt 5.15.13, Coin 4.0.2, Vtk 9.2.6, OCC 7.7.2  
Locale: English/United Kingdom (en_GB)   

Thus the sequence to generate a wing and a drawing is:
- place the macro and data files in some folder and
  modify the path in the macros.
- define the wing geometry in wDat19928.lis 
- start FreeCAD 18 and create a new file, which will
  be called "unnamed" (without quotes). Now run the  
  mkRibAutoStrt9.FCMacro                           -> inner and outer wing lofts are generated
- save the file and load it in FreeCAD 21.x and  
  run mkRibAuto9.FCMacro                           -> wing ribs are generated      
- edit prnObj9.FCMacro, set kB to 1 (or any value > 0) 
  and give the name and path of the output file.
  Running prnObj9 will generate a list of all objects in 
  the wing file. In this exampel the file is objetcs9.lis
- make a copy of the object file generated in the previous
  step and open it. Find the object names of the ribs by
  highlighting them from tip to root. Enter a number from
  1 to nRib in column 3 of your copied object file. Save the 
  file. The copied objet file now looks like prnObjList9.lis 
- edit prnObj9.FCMacro by giving the name and path of the
  object input file generated in the previous step, then
  set kB to -1 and run prnObj9. This will generate a page
  containing all ribs that had a number assigned to them
  in the copy of the object file.


Happy Modeling Everyone!

Juergen
