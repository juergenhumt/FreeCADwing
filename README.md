

FreeCADwing is a sequence of macros for FreeCAD that allow you to generate a tapered wing, the wing ribs and place the ribs in a drawing which you can export as an svg file to create e.g. the input for a laser cutter. You have to recolour the rib edges manually to red RGB = [255,0,0] for a laser cutter

First define the wing geometry in file wDat19928.lis (filename is, of course, arbitrary), it contains the data for both inner and outer wing section. Line 0, the first line, is no longer used. Outer wing data start in line 8, after the first nRig.

The program files are in a directory FreeCADwing, there ar two sub directories called data and ex1. The data subdirectory is used to exchange information between the the different parts of the program. It contains a binary file that stores the path of the current work directory and the current project name. ex1 is the work directory for the test case, you add other project sub directories for yor own porjects.

FreeCADwing was tested using FreeCAD version 1.0.0

A)    Run the Test
To create the wing for the test case where the project name is MonoWingMk2
- FreeCadWingStart.FCMacro -> generates the two wing sections and lofts the profiles
  on my computer it took abour 2 to 3 minutes to generate the wing loft. If you delete
  it though and rerun it only takes 2 or 3 seconds to generate the loft. I have no
  idea why that is. Now run:
- FreeCadMkRib.FCMacro     -> generates the ribs
- FreeCadMkRib writes a file called obj<projName>.lis,
  hence the file name is objMonoWingMk2.lis. In the 
  general case you have to edit this file, see below
- for the test case a modified file objMonoWingMk2_mod.lis 
  has been provided, which is used in the next step, so now run
- FreeCadPrn.FCMacro -> generates a plot of all wing ribs and 
  saves the plot as an svg file.

To get familiar with the obj files you might want to compare the objMonoWingMk2.lis and objMonoWingMk2_mod.files. 

B)    Use FreeCADwing for your own projects
In the general case after the first two macros, before running FreeCadPrn.FCMacro, the file containing the objects has to be edited. Copy the obj<projName>.lis file to obj<projName>_mod.lis i.e. add _mod to the name of the object file. Open the file while you have opended your project model in FreeCAD 

If the test case has generated the file MonoWingMk2.FCStd and the
svg file .......svg you can
sequence to generate a wing and a drawing is:
- create a new sub directory for your project.
- palce the profile data files there and the wing geometry
  data file. Give the data file a name of your choice
- modify the project name and the path to your work directory
  in the macro FreeCadWingStart.FCMacro. This information will
  be stored in data subdirectory in the binary file projData.lis 
  and will be used by the other modules.
- define the wing geometry in the wing geometry file, which,
  for the test case, is called wDat19928.lis, then run
- FreeCadWingStart.FCMacro -> generates the two wing sections and lofts the profiles, now run
- FreeCadMkRib.FCMacro     -> generates the ribs and a file obj<prjName>.lis
- make a copy of the object file generated in the previous
  step and modify the name to obj<prjName>_mod.list. Go to
  FreeCAD and find the object names of the ribs by
  highlighting them from tip to root. Enter a number from
  1 to nRib in column 3 of your copied object file. Save the 
  file. The copied objet file now looks like objMonoWingMk2_mod.lis 
- now run FreeCadWingPrn.FCMacro, this will generate a page
  containing all ribs that had a number assigned to them
  in the copy of the object file. You can export this page
  to an svg file. If you want to use it as input to e.g. a
  laser cutter you have to set the line colour manually to
  rgb [0,0,255]
