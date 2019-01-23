#!/opt/pxsoft/bin/cctbx.python
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 15:05:14 2018

@author: foos
"""
#Module converter:*.mtz amplitudes files to XDS_ASCII.HKL intensities  

from os import path
from sys import argv
from iotbx.file_reader import any_file
from cctbx import miller
from cctbx import crystal 


    
output_path=argv[1]
input_file=argv[2]
try:
    argv[3]
except:
    ano=False
else:
    if argv[3] == "-a":
        ano=True
    else:
        ano=False

output_name= input_file.split("/")[-1]
def importer_converter(output_path, input_file, outputname, ano):

    f= any_file(input_file, force_type="hkl")
    miller_array= f.file_server.miller_arrays
    array_num= len(miller_array)

    i = array_num-1
    while i >= 0:
        fobs= miller_array[i]
        if str(fobs.info()).split(":")[1] == "F(+),SIGF(+),F(-),SIGF(-)" and ano is True:
            print "it's amplitude with ANO"
            fobs= fobs.as_anomalous_array()
            iobs= fobs.f_as_f_sq()
            break
        elif str(fobs.info()).split(":")[1] == "FOBS,SIGFOBS":
            print "it's amplitude"
            iobs= fobs.f_as_f_sq()
            break
        elif str(fobs.info()).split(":")[1] == "I(+),SIGI(+),I(-),SIGI(-)" and ano is True:
            print "it's already ANO intensity"
            fobs= fobs.as_anomalous_array()
            iobs= fobs
            break
        elif str(fobs.info()).split(":")[1] == "IOBS,SIGIOBS":
            print "it's already intensity"
            iobs= fobs
            break
        i-=1
#    i = 0
#    while i < 4:
#        fobs= miller_array[i]
#        if str(fobs.observation_type())== "xray.amplitude":
#            print "it's amplitude"
#            #convert amplitudes in intensities
#            iobs= fobs.f_as_f_sq()
#            break
#        elif str(fobs.observation_type()) == "xray.intensity":
#            print "it's already intensity"
#            iobs= fobs
#            break
#        #elif str(fobs.observation_type()) == "None":        
#        #    continue
#        i+=1
        
     
        
         
    # following command return type of data (amplitudes, intensities...)
    #print fobs.observation_type()
    
    #fobs.show_summary()
    
    
    i_table= []
    for i in iobs:
         i2= list(i)
         i2[1]= '%.3E' % i2[1]
         i2[2]= '%.3E' % i2[2]
         i= tuple(i2)
         i_table.append(i)
        
    
    #preparing file 2 output and create output
    
    line= []    
    for i in i_table:
            i2=str(i).replace("'", '')
            line.append(i2)    
           
    line2= []
    for i in line:
        i2=i.replace("(",'')
        i3=i2.replace(")",'')
        i4=i3.replace(",",'')
        line2.append(i4)
    
    
    line2.insert(0,"!END_OF_HEADER")
    line2.insert(0,"!ITEM_SIGMA(IOBS)=5")
    line2.insert(0,"!ITEM_IOBS=4")
    line2.insert(0,"!ITEM_L=3")
    line2.insert(0,"!ITEM_K=2")
    line2.insert(0,"!ITEM_H=1")
    line2.insert(0,"!NUMBER_OF_ITEMS_IN_EACH_DATA_RECORD=5")
    
    cell= str(iobs.unit_cell())
    cell1= cell.replace("(",'')
    cell1= cell1.replace(")",'')
    cell2= cell1.replace(",",'    ')
    
    line2.insert(0,"!UNIT_CELL_CONSTANTS=     "+cell2)
    line2.insert(0,"!SPACE_GROUP=    "+str(iobs.space_group_info()))
    
    res= str(iobs.d_max_min())
    res1= res.replace("(",'')
    res1= res1.replace(")",'')
    res1= res1.replace(",",'     ')
    #line2.insert(0,"!INCLUDE_RESOLUTION_RANGE=     "+res1)
    
    if iobs.anomalous_flag() is True:
        line2.insert(0,"!FORMAT=XDS_ASCII    MERGE=TRUE    FRIEDEL'S_LAW=FALSE")
    else:
        line2.insert(0,"!FORMAT=XDS_ASCII    MERGE=TRUE    FRIEDEL'S_LAW=TRUE")
    
    line2.append("!END_OF_DATA")
    
    outputfile= open(str(output_path)+"/"+str(output_name)+".hkl", 'a')

    
    for i in line2:
        outputfile.write(i+ "\n")
    #print path+"/"+str(input_file)+".hkl"
importer_converter(output_path, input_file, output_name, ano)
