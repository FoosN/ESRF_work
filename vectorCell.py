# -*- coding: utf-8 -*-
"""
Spyder Editor

This temporary script file is located here:
/users/foos/.spyder2/.temp.py
"""
import sys
import os
#import re
import numpy as np
#import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


maninput_files = []
for arg in sys.argv[1:]:
    try:
        if os.path.isfile(arg):
            f = open(arg)
            lines = f.readlines()
            f.close()
            if ("XPARM.XDS" in lines[0]):
                maninput_files.append(arg)
    except:
        pass

path2 = []
tpath = []
tpath2 = []
tpath3 = []
for arg in sys.argv[1:]:
    try:
        if arg == "weeded_files.txt":
            path1 = os.path.abspath(arg)
            path1 = path1.split('/')
            del path1[-1]
            path1 = '/'.join(path1)+'/'
            with open(arg) as weeded_file :
                lines = weeded_file.readlines()
                f2find = lines
            f2find=f2find[2:]
            for f in f2find:
                path2.append(path1+f[:-1])
            for p in path2:
                tpath.append(os.path.realpath(p))
            for i in tpath:
                index = tpath.index(i)
                tpath2.append(tpath[index].split('/'))
                del tpath2[index][-1]
            for i in tpath2:
                index = tpath2.index(i)
                tpath3.append('/'.join(tpath2[index])+'/GXPARM.XDS')
            maninput_files = tpath3 
    except:
        pass
#print maninput_files

for arg in sys.argv[1:]:
    path= os.path.abspath(arg)
for root, dirs, files in os.walk(path):
    for filename in files:
        if "GXPARM" and ".XDS" in filename:
            maninput_files.append(os.path.join(root, filename))

#            

######      define lab coord. of unit cell a, b and c axis
def fromGXPARMtoarray(maninput_files):
    crystList = []  
    j = 0
    for i in maninput_files :
         with open(i) as inputfile:
             lines = inputfile.readlines()
         table = lines[4:7]
         j+=1
         table2 =[]
         print table, 'file number :', j
         for i in table:
             table2.append(i.split())
         vecta =np.array([float(table2[0][0]), float(table2[0][1]), float(table2[0][2])])
         vectb =np.array([float(table2[1][0]), float(table2[1][1]), float(table2[1][2])])
         vectc =np.array([float(table2[2][0]), float(table2[2][1]), float(table2[2][2])])
         vectRes =vecta+vectb+vectc
         crystList.append(vectRes)
         
                 
    return crystList

crystList = fromGXPARMtoarray(maninput_files)
##maxvalue = np.amax(crystList)
#minvalue = np.amin(crystList)

######    control of the magnitude off the vectors (have to be identical)
vectMagn = []
for i in crystList:
    magn=np.sqrt(np.vdot(i,i))
    vectMagn.append(magn)
fig = plt.figure()
ax = fig.add_subplot(111)
for i in vectMagn:
    ax.scatter(vectMagn.index(i), [i], c='r', marker= '^')
plt.show()
########    create the list of vector 2D from the crystList (contain 3D vector)
#
#vector2D=[]
#for i in crystList:
#    vector2D.append([0,0,i[0],i[1]])
#
#vector = np.array(vector2D)
#X,Y,U,V = zip(*vector)
#plt.figure()
#ax = plt.gca()
#ax.quiver(X,Y,U,V,angles='xy',scale_units='xy',scale=1)
#ax.set_xlim([np.amin(U)-10,np.amax(U)+10])
#ax.set_ylim([np.min(V)-10,np.amax(V)+10])
#plt.draw()
#plt.show()
#
#######    3D plot scattering. (using Sum vector from crystList)
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#for i in crystList:
#    ax.scatter(i[0], i[1], i[2], c='y', marker='d')
#ax.set_xlabel('X')
#ax.set_ylabel('Y')
#ax.set_zlabel('Z')
#
#plt.show()  
#
#########    2D plot scattering (using Sum vector orthogonal projection along z)
#fig = plt.figure()
#ax = fig.add_subplot(111)
#for i in crystList:
#    ax.scatter(i[0], i[1], c='b', marker='o')
#plt.show()


####### 3D plot vectors
vector3D=[]
for i in crystList:
    N = np.sqrt(np.vdot(i,i))
    vector3D.append([0,0,0,i[0],i[1],i[2], N])
#
######## WARNING : magnitude for represented vectors is arbitraty parametered see following :
#lenVect = np.average(N)
vector = np.array(vector3D)
#X,Y,Z,U,V,W,N = zip(*vector)
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#s = ax.quiver(X,Y,Z,U,V,W, length = lenVect, colors='b', arrow_length_ratio=0.05, pivot='middle')
##ax.quiver(X,Y,Z,U,V,W,W, cmap=plt.cm.gray, arrow_length_ratio=0.05, zorder=4, pivot='middle')'
#ax.set_xlim([-lenVect-10, lenVect+10])
#ax.set_ylim([-lenVect-10, lenVect+10])
#ax.set_zlim([-lenVect-10, lenVect+10])
#ax.patch.set_facecolor('0.7')
#
#plt.draw()
#plt.show()
#
#
##### export table with vector for pymol
#print "this is the table of vector : ", vector3D

def writing_list_in_file(path, file2write):
    outputfile = open(os.path.join(path, "arrow4pymol.txt"), 'a')
    for line in file2write:    
        outputfile.write("cgo_arrow "+line+'\n')

file2write = []
for i in vector3D: 
    coord = '['+str(i[0]-0.5*i[3])+','+str(i[1]-0.5*i[4])+','+str(i[2]-0.5*i[5])+'],['+str(0.5*i[3])+','+str(0.5*i[4])+','+str(0.5*i[5])+']'
#    coord = '['+str(i[0])+','+str(i[1])+','+str(i[2])+'],['+str(i[3])+','+str(i[4])+','+str(i[5])+']'
    file2write.append(coord)

writing_list_in_file(".", file2write)
    

