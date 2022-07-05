import pandas as pd
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style

electric_current=[]
Voltage=[]
TIME=[]
path = 'E:/Industey-log-data/MSPS/FireData/'
def read_log():
    list1=[]
    list2=[]
    list3=[]
    log = open(fileaddresstlog, 'r')
    count=0
    for logline in log:
        if count>8:
            logline = logline.split('	')
            list1.append(logline[2])
            list2.append(logline[1])
            list3.append(logline[0])
        count=count+1
    return list1,list2,list3

# 文件列表
files = []
for file in os.listdir(path):
    if os.path.isfile(file):
        if file.endswith(".gdf"):
            files.append(path + file)
    else:
        for file1 in os.listdir(path+file+'/'):
            if file1.endswith(".gdf"):
                files.append(path + file+'/' +file1)


data = pd.DataFrame()
def unified_dimension_Y(List1):
    arr_sum=1
    newdata=[]
    for i in range(len(List1)):
        arr_sum=arr_sum+float(List1[i])
    for i in range(len(List1)):
        newdata.append(float(List1[i])/arr_sum)
    return newdata

def PLOT_Vol():
    for r in range(len(TIME)):
        # electric_current[r]=electric_current[r]/sum(electric_current[r])
        new_Voltage = unified_dimension_Y(Voltage[r])
        plt.plot(TIME[r], new_Voltage)
    plt.show()
def PLOT_ELE():
     for r in range(len(TIME)):
        new_electric_current=unified_dimension_Y(electric_current[r])
        plt.plot(TIME[r], new_electric_current)
     plt.show()
if __name__ == '__main__':
    r=0
    for fileaddresstlog in files:
        List1,List2,List3=read_log()
        electric_current.append(List1)
        Voltage.append(List2)
        TIME.append(List3)
   # PLOT_ELE()
    PLOT_Vol()
    print('end')