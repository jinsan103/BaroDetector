# feature extraction: Rate of change, Mean-crossing, Standard deviation
# Silding window size: 30
# overlap: 0.5 sec


import os
import numpy as np
import statistics as stat
import csv
import sys


def getZeroCrossingRate(arr):
    np_array = np.array(arr)
    return float("{0:.4f}".format((((np_array[:-1] * np_array[1:]) < 0).sum()) / len(arr)))


def getMeanCrossingRate(arr):
    return getZeroCrossingRate(np.array(arr) - np.mean(arr))


def getRateOfChange(arr,first,last):
    np_array = np.array(arr)
    return (np_array[last]-np_array[first])/window_size
    #return (np_array[1:] / np_array[:-1] - 1).sum()

window_size = 30
overlap = 0.5
LABEL_IN = "Indoor"
LABEL_OUT = "Outdoor"
LABEL_PASSING = "Passing"
window_arr_pressure = []
window_arr_label = []
roc = []
mcr = []
std = []
label = []

if __name__=="__main__":
    for root, dirs, files in os.walk("./"):
        for file_name in files:
            if os.path.splitext(file_name)[-1] == '.csv': # Depends on file type
                with open(file_name, 'r',encoding = 'ISO-8859-1') as f:
                    reader = csv.reader(f)
                    for txt in reader:
                        #vals = line[:-1].split(",") # 맨 끝의 \n 제외한 것들을 , 기준으로 나눔
                        window_arr_pressure.append(float(txt[1]))
                        window_arr_label.append(txt[2])
                    for index, line in enumerate(window_arr_pressure):
                        if 29 < index and index % 5 is 0: #need to overlap 5
                            roc.append(float(getRateOfChange(window_arr_pressure,index-29,index))) # Rate of change
                            mcr.append(float(getMeanCrossingRate(window_arr_pressure[index-29:index]))) # MCR from previous 30 num of data
                            std.append(float(stat.stdev(window_arr_pressure[index-29:index]))) # STD from previous 30 num of data
                            label.append(window_arr_label[index]) # each label
                    window_arr_pressure = []
                    window_arr_label = []
                
    
    with open('./arff_files/'+'result.arff','w',newline='') as f: # make arff file format
        f.write('''@RELATION pressure
                    
@attribute roc numeric
@attribute mcr numeric
@attribute std numeric
@attribute label {Indoor, Outdoor, Passing}

@data
''')
        for index, line in enumerate(roc):
            f.write(str(roc[index])+","+str(mcr[index])+","+str(std[index])+","+label[index]+"\n")
