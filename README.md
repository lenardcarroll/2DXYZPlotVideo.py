# 2DXYZPlotVideo.py

This python script makes a simple XY plot of a .xyz file that has at least 1 frame. The script command has a general command of:

```python -i 2DXYZPlotVideo.py -in <INPUTSTRUCTURE> -sk <SKIPVALUE> -fr <RANGE-OF-FROZEN-ATOMS> -ig <T or F>```
  
where ```<INPUTSTRUCTURE>``` is the user's input .xyz file, ```<SKIPVALUE>``` is the how many frames should be skipped at a time, ```<RANGE-OF-FROZEN-ATOMS>``` is the range of atoms that are fixed in the .xyz file (these atoms are blacked out) and ```-ig <T or F>``` is for choosing to either remove the frozen atoms (T) in the plotting, or to keep them (F). 

The default for -sk is 1 (no frame is skipped), the default for -fr is 0, therefore no atoms are frozen or chosen to be blacked out, and the default for -ig is F, therefore no atoms are removed from the plot(s). 
  
## Example of the use of 2DXYZPlotVideo.py
  
A typical plot generated from 2DXYZPlotVideo.py looks like:
![2DXYZPlotVideo.py Example Plot](https://raw.githubusercontent.com/lenardcarroll/2DXYZPlotVideo.py/main/frame_0.jpg "Example of plot from 2DXYZPlotVideo.py")
  
All the plots have the same x-y labels, has a legend which shows which circle corresponds to which atom, displays the minimum and maximum z value from the frame and includes some grids as to see exactly how the atoms are moving over time (more specific). Extra space is placed around every frame as to ensure that the plot won't change in size over time, messing up the video (play around with the sizes if that does happen). The size of the atoms has been chosen as either the empirical or the estimated radius of every atom, multipled by 4. Since this is a 2D plot that is supposed to contain depth (there are various z-values), the size of the atoms are changed according to the equation:

R = r + z*tan(&theta;)
 
where R is the radius of the target circle, r is the radius of the bottom most circle, z is the z-value of the target atom and tan(&theta;) = 3r/20. Therefore, the final equation is:
  
R = (3z+20)r/20
  
The bigger the distance between two atom types are, the bigger the size difference. Although the above is to determine the change in the atom size as the z value changes, all the sizes are also multiplied by the value (19.6/6.4)<sup>2 = 9. This is since the default plot size is 6.4x4.8, and readjusting the plot size to 19.6x14.4 meant that points had to increase by (19.6/6.4)<sup>2. If you want to change the plot size (make it bigger or smaller), then you'll have to change the following:
```
ax.scatter(x.iloc[i],y.iloc[i],c=col[i],s=size[i]*int(((19.2/6.4))**2),edgecolors='black',marker='o',lw=2)
plt.legend(handles=[eval(atom_labels(i)) for i in atom_types],bbox_to_anchor=(1,1), loc="upper left",fontsize=20)
plt.xlabel("x-coordinates (in Å)",fontsize=20)
plt.ylabel("y-coordinates (in Å)",fontsize=20)
plt.yticks(fontsize=20)
plt.xticks(fontsize=20)
plt.gcf().set_size_inches(19.2, 14.4)
```

When changing the size of the plot (last line above), you'll also want to subsequently change the size of the circle ```s=size[i]*int(((19.2/6.4))**2)``` (just replace 19.2 with your new plot width) and the font size in the plot.
  
