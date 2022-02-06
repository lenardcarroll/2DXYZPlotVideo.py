#Load in All The Modules Needed
import argparse
import pandas as pd
import numpy as np
import csv
import os
from os import path
import shutil
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.offsetbox import AnchoredText
import multiprocessing
from multiprocessing import Pool
import cv2

#Arguments Cheat/Help Sheet
parser = argparse.ArgumentParser()
parser.add_argument("-in", "--input", dest = "input", default = "input.xyz", help="Name of the input file")
parser.add_argument("-sk", "--skip", dest = "skipvalue", default = "1", help="Reads in every nth frame, were n is specified by the user. 1 is the default where every frame is read in.")
parser.add_argument("-fr", "--frozen", dest = "frozenrange", default = "0", help="The range of atoms that are frozen. If none are frozen, specify 0 or ignore the flag. Must be written as 'X-Y'")
parser.add_argument("-ig", "--ignore", dest = "ignorefrozen", default = "F", help="Specify if the frozen atoms should be removed from the frames or not. F is to keep, T is to remove the atoms.")
args = parser.parse_args()

#Determines the number of atoms each frame of the system has
with open(args.input) as f:
    lines = f.read()
    first = lines.split('\n', 1)[0]

ignorefrozen = args.ignorefrozen #Should the frozen atoms be removed or not?
num_of_atoms, num_of_lines = int(first), len(list(open(args.input))) #First specifies number of atoms, the second calculates the number of lines in the xyz file
num_of_frames  = int(num_of_lines/(num_of_atoms+2)) #Calculates the number of frames for the xyz file
skipvalue = int(args.skipvalue) #What is the skip sequence as specified by the user?
frozenrange, firstval, lastval, dash = args.frozenrange, -2, -2, -2 # First value is the range of frozen atoms as specificied by the user, the other values are just to initialize the other terms

#Here the range of frozen atoms is properly stored
if '-' in frozenrange:
    dash = frozenrange.index('-')
    firstval = int(frozenrange[:dash])
    lastval = int(frozenrange[dash+1:])
elif int(frozenrange)==0:
    firstval = -2
    lastval = -1
else:
    firstval = int(frozenrange)
    lastval = firstval

#This cuts out the headers of each frame
skiparray = []
for i in range(num_of_frames):
    k = num_of_atoms*i+2*i
    skiparray.append(k)
    skiparray.append(k+1)
df = pd.read_csv(args.input, skiprows=skiparray, names=['Atom', 'X', 'Y', 'Z'], sep="\s+" , engine='python')

#This splits the dataframe into frames
frames = [ df.iloc[i*num_of_atoms:(i+1)*num_of_atoms].copy() for i in range(num_of_frames+1) ]

#This resets the index of each frame
for i in range(0,num_of_frames,skipvalue):
    frames[i] = frames[i].reset_index(drop=True)

#Now we create a folder named Images where the Images will be later saved to
directory = "Images"
parent_dir = "."
if os.path.exists("./Images") == False:
    outpath = os.path.join(parent_dir, directory)
    os.mkdir(outpath)
else:
    shutil.rmtree("./Images")
    outpath = os.path.join(parent_dir, directory)
    os.mkdir(outpath)

#We setup the plot here
fig,ax = plt.subplots()
x, y, z = frames[0]['X'], frames[0]['Y'], frames[0]['Z']
plt.rc('grid', linestyle=':', color='gray', linewidth=1)
min_X, min_Y = min(frames[0]['X']), min(frames[0]['Y'])
min_X, min_Y = min_X - 4, min_X - 4
max_X, max_Y = max(frames[0]['X']), max(frames[0]['Y'])
max_X, max_Y = max_X + 4, max_Y + 4

#The lists below are storing all the elements of the periodic table, their size for the plot and the color assigned to them. The color was randomly chosen.
ptable = ['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn','Fr','Ra','Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og','Un']
colorlist = ['#ADADAD', '#0578c6', '#838931', '#e82e6a', '#e58918', '#404040', '#004A7F', '#FF0000', '#c70102', '#bfdf85', '#013e99', '#98f7c6', '#ee383d', '#d5a4ca', '#b3c8be', '#960892', '#fb7a9d', '#26d389', '#5ebc33', '#89263e', '#10f9bd', '#bee760', '#205df5', '#b10bab', '#4163da', '#9ca948', '#31a9f3', '#b33d74', '#FF6A00', '#30ff79', '#b7d1b8', '#a092bc', '#8139f6', '#57ffd2', '#21685d', '#9eb570', '#4ccf48', '#41be51', '#2f1861', '#c90799', '#508a1d', '#7c1464', '#48a64b', '#31fa8e', '#9e5fbd', '#c77094', '#7f60b7', '#f66f74', '#715856', '#d221e4', '#de99e2', '#29c2a9', '#6069c2', '#0cc49d', '#642786', '#e405b6', '#560dd3', '#7006d7', '#f04d9d', '#5c1b63', '#cb920f', '#61521a', '#e6da8a', '#da25bc', '#bd4b95', '#94a8ec', '#f054a6', '#bc7424', '#b6582d', '#494d80', '#239f1f', '#3d738d', '#cf9c04', '#77b7c7', '#e6a211', '#c6f2cb', '#246d90', '#054298', '#FFD800', '#2e0e29', '#b03d4b', '#612d01', '#347408', '#65d366', '#057faf', '#69cf90', '#587960', '#24d8c0', '#ac6a12', '#58226c', '#ac851a', '#97adf3', '#da8f0c', '#726883', '#bb7b8b', '#40150a', '#a6c2b6', '#790946', '#38232e', '#41e8c0', '#41d468', '#4edd68', '#3f2fb9', '#3082a8', '#3cbd53', '#4b9395', '#29bdf3', '#d40c42', '#2c219c', '#6de5ef', '#d7cd83', '#6ef13a', '#e03729', '#677b60', '#632e7e', '#9a265a', '#741b0c', '#261741','#000000']
radiuslist = [100, 60, 580, 420, 340, 280, 260, 240, 200, 160, 720, 600, 500, 440, 400, 400, 400, 284, 880, 720, 640, 560, 540, 560, 560, 560, 540, 540, 540, 540, 520, 500, 460, 460, 460, 440, 940, 800, 720, 620, 580, 580, 540, 520, 540, 560, 640, 620, 620, 580, 580, 560, 560, 540, 1040, 860, 780, 740, 740, 740, 740, 740, 780, 720, 700, 700, 700, 700, 700, 700, 700, 620, 580, 540, 540, 520, 540, 540, 540, 600, 760, 720, 640, 760, 800, 840, 1120, 860, 780, 720, 720, 700, 700, 700, 700, 700, 700, 680, 680, 680, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660, 660]

#Function to get the color of the atom
def atom_color(X):
    return colorlist[ptable.index(X)]

#Function to get the color and label for the atom plot legend
def atom_labels(X):
    if X == 'Un':
        label = 'Frozen'
    else:
        label = X
    color = atom_color(X)
    return "mpatches.Patch(color='%s', label='%s')" % (color,label)

#Function to determine the size of the atom in the plot
def atom_size(X):
    return radiuslist[ptable.index(X)]

#Function used to make the plot of the frames
def f(j):
    ax.clear() #clears the plots as to make sure multiple plots aren't made on the same file
    frozen_atoms = []
    for i in frames[j].index:
        if i in range(firstval-1,lastval):
             frozen_atoms.append('T')
        else:
             frozen_atoms.append('F')
    frames[j].insert(loc=3, column='Frozen', value=frozen_atoms) #Here is added information on which atoms are frozen or not
    if ignorefrozen == 'T': #If atoms are frozen and the user wants to ignore it in the plot, here the ignored atoms are removed from the dataframe
        frames[j] = frames[j].drop(frames[j].index [ range(firstval-1,lastval) ])
    col = []
    frames[j] = frames[j].sort_values(by ='Z', ascending = True) #The dataframe is sorted as to have the atom with the minimum z value at the top of the dataframe, while the one with the maximim z value at the bottom
    frames[j] = frames[j].reset_index(drop=True) #The index of the dataframe is once again reset
    for i in frames[j].index: #If the user did not ignore the frozen atoms, here it specificies if the frozen atoms should be blacked out
        if frames[j]['Frozen'].iloc[i] == 'T':
            col.append('black')
        else:
            col.append(atom_color(frames[j]['Atom'].iloc[i]))              
    x, y, z = frames[j]['X'], frames[j]['Y'], frames[j]['Z']
    size = []
    min_Z = min(frames[j]['Z'])
    z_alt = z - min_Z

    #Here the size of the atoms in the plot are put together
    for i in frames[j].index:
        size.append(atom_size(frames[j]['Atom'].iloc[i])+2*z_alt.iloc[i]*np.tan(np.arctan((atom_size(frames[j]['Atom'].iloc[i])/0.6-atom_size(frames[j]['Atom'].iloc[i]))/(2*10))))
    #Here the plot is made, with a black border around the points
    for i in range(len(col)):
        ax.scatter(x.iloc[i],y.iloc[i],c=col[i],s=size[i]*int(((19.6/6.4)+0.5)**2),edgecolors='black',marker='o',lw=2)
    #Creates 4 A space all around the outer atoms as to not have it disappear when atoms move out of frame
    ax.set_ylim(min_Y,max_Y)
    ax.set_xlim(min_X,max_X)
    atom_types = []
    #Here the labels of atoms are put together
    for i in frames[j].index:
        if frames[j]['Frozen'].iloc[i] == 'T':
            if 'Un' not in atom_types:
                atom_types.append('Un')
        if frames[j]['Atom'].iloc[i] not in atom_types and frames[j]['Frozen'].iloc[i] == 'F':
            atom_types.append(frames[j]['Atom'].iloc[i])
    plt.legend(handles=[eval(atom_labels(i)) for i in atom_types],bbox_to_anchor=(1,1), loc="upper left",fontsize=20)
    plt.grid(True)
    plt.xlabel("x-coordinates (in Å)",fontsize=20)
    plt.ylabel("y-coordinates (in Å)",fontsize=20)
    plt.yticks(fontsize=20)
    plt.xticks(fontsize=20)
    plt.gcf().set_size_inches(19.6, 14.4)
    #Minimum and maxmum z values are plotted as to keep track how the z component is changing
    anchored_text = AnchoredText("min_Z = %0.5f\nmax_Z = %0.5f" % (min_Z,max(frames[j]['Z'])), loc="lower left")
    ax.add_artist(anchored_text)
    plt.draw()
    fig.savefig(path.join(outpath,"frame_{00}.jpg".format(j)),bbox_inches ="tight")

#Multiprocessing is used to make the plots and a video at the end of the plots
if __name__ == '__main__':
    pool = multiprocessing.Pool(4)
    pool.map(f, range(0, num_of_frames, skipvalue))

    image_folder = 'Images'
    video_name = 'video.avi'
    images = []
    for i in range(0,num_of_frames,skipvalue):
        images.append('frame_%d.jpg' % i)
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, 0, 24, (width,height))
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))
    cv2.destroyAllWindows()
    video.release()
