# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 15:05:14 2018

@author: foos
"""
import os
import re



def build_xdsfile_list(pattern,start_directory,startnumber):
    Fcount = 0
    find_files = True
#    if os.path.isfile(config_file):
#        print "WARNING -- REMOVING CONFIG FILE"
#        os.remove(config_file)
    xdsfiles = []
    if find_files:
        Fcount=startnumber;
        print "Find files mode.  Looking for files ending with "+pattern+" in "+start_directory
        for root, dirs, files in os.walk(str(start_directory),followlinks=True):
            for file in files:
#                if file.endswith("ASCII.HKL"):
#                ext = ["s1.HKL","s2.HKL"]
#                if file.endswith(tuple(ext)):
#                if file.endswith("deisa"):
#                 if file.endswith(pattern):
                 source =  os.path.join(root, file)
                 if re.search(pattern,str(source)):

                    print(os.path.join(root, file))
                    target = str(Fcount)+".HKL"
                    print "SOURCe "+str(source)+" TARGET "+str(target)
                    if os.path.exists(target):
                        print "Hmm... "+target+" already exists"
                        if os.path.islink(target):
                            print "Clobbering link "+target
                            os.remove(target)
                        else:
                            print "Could not set up links:  the target file "+target+" already exists.  Please delete it!"
                            exit
                    os.symlink(str(source),target)
                    xdsfiles.append(str(Fcount)+".HKL")
                    Fcount = Fcount +1
#    else:
#        xdsfiles = glob.glob("*.HKL")
#        xdsfiles.append(glob.glob("*.hkl"))
    return xdsfiles,Fcount    

def cell_and_sg_from_XDS_ASCII (xdsfile):
    sgn=""
    cell=""
#    print "XDS FILE "+str(xdsfile)
    XDS = open(xdsfile)
    SG = re.compile('\!SPACE_GROUP_NUMBER=\s+(\d+)')
    UCELL = re.compile('\!UNIT_CELL_CONSTANTS=\s+(.*)')
    for item in XDS.readlines():
        if SG.match(item):
            matches = SG.search(item)
            sgn=matches.group(1)
        if UCELL.match(item):
            matches = UCELL.search(item)
            cell=matches.group(1)
    return (sgn,cell)  



def resolution_setup(resMax):
    res_range = "INCLUDE_RESOLUTION_RANGE=100 "+str(resMax)+" \n"
    return res_range


def minimum_options():
    output = "OUTPUT_FILE=all_merge.hkl \n"
    merge = "MERGE=TRUE \n"
    friedel = "FRIEDEL'S_LAW=TRUE \n"
    procNumb = "MAXIMUM_NUMBER_OF_PROCESSORS=8 \n"
    saveImg= "SAVE_CORRECTION_IMAGES=FALSE \n"
    return output, merge, friedel, procNumb, saveImg
    

def writing_list_in_file(path, file2write):
    """ Function to write string contain in a list 
    """    
    outputfile = open(os.path.join(path, "XSCALE.INP"), 'a')
    for line in file2write:    
        outputfile.write(line)


file2write=[]
resMax= 1.3
res_range = resolution_setup(resMax)
output, merge, friedel, procNumb, saveImg = minimum_options()
my_xdslist, my_number = build_xdsfile_list("REPROC.HKL", "./", 0)
cellSG = cell_and_sg_from_XDS_ASCII ("0.HKL")
cell = "UNIT_CELL_CONSTANTS="+str(cellSG[1])+" \n"
SG = "SPACE_GROUP_NUMBER="+str(cellSG[0])+" \n"
file2write.append(output)
file2write.append(merge)
file2write.append(saveImg)
file2write.append(cell)
file2write.append(friedel)
file2write.append(SG)
file2write.append(procNumb)
for i in my_xdslist:
    file2write.append("INPUT_FILE="+str(i)+" XDS_ASCII \n")
    file2write.append(res_range)
    file2write.append("MINIMUM_I/SIGMA= 0 \n")

writing_list_in_file(".", file2write)    
os.system("xscale_par")
