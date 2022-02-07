# 2DXYZPlotVideo.py

This python script makes a simple XY plot of a .xyz file that has at least 1 frame. The script command has a general command of:

```python -i 2DXYZPlotVideo.py -in <INPUTSTRUCTURE> -sk <SKIPVALUE> -fr <RANGE-OF-FROZEN-ATOMS> -ig <T or F>```
  
where <INPUTSTRUCTURE> is the user's input .xyz file, <SKIPVALUE> is the how many frames should be skipped at a time, <RANGE-OF-FROZEN-ATOMS> is the range of atoms that are fixed in the .xyz file (these atoms are blacked out) and -ig <T or F> is for choosing to either remove the frozen atoms (T) in the plotting, or to keep them (F). 

The default for -sk is 1 (no frame is skipped), the default for -fr is 0, therefore no atoms are frozen or chosen to be blacked out, and the default for -ig is F, therefore no atoms are removed from the plot(s). 
  
#An example of 
