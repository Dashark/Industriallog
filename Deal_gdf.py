import pandas as pd
import numpy as np
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style

electric_current=[]
Voltage=[]
TIME=[]
MOD=[]
path = 'E:/Industey-log-data/MSPS/FireData/'#可以把测试样例下载下来改成时间文件夹前面的地址
def read_log():
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    log = open(fileaddresstlog, 'r')
    count=0
    for logline in log:
        data1={}
        if count<=8:
            logline1=logline.split(':')
            data1[logline1[0]]=logline1[1].strip('/n')
            list4.append(data1)
        else:
            logline = logline.split('	')
            list1.append(logline[2])
            list2.append(logline[1])
            list3.append(logline[0])
        count=count+1
    return list1,list2,list3,list4

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
def PLOT_ELE(time1,elec1,date):
    for r in range(len(time1)):
        #new_electric_current=unified_dimension_Y(elec1[r])
        #time=float(date)+float(time1)
        time2=[]
        for i in range(len(time1[r])):
            x=float(time[r][i])+float(date[r])
            time2.append(x)
        plt.plot(time2, elec1[r])
    plt.show()
def extract(id_no):
    temp_time=[]
    temp_elec=[]
    temp_volt=[]
    temp_datetime=[]
    for i in range(len(TIME)):
        str_id=str(MOD[i][1].values()).strip('dict_values([\'')
        str_id=str_id.replace("\\n\'])",'')
        if id_no==str_id:
            str_date = str(MOD[i][4].values()).strip('dict_values([\'')
            str_date = str_date.replace("\\n\'])", '')
            temp_datetime.append(str_date)
            temp_time.append(TIME[i])
            temp_elec.append(electric_current[i])
            temp_volt.append(Voltage[i])
    return temp_time,temp_elec,temp_volt,temp_datetime
if __name__ == '__main__':
    r=0
    for fileaddresstlog in files:
        List1,List2,List3,List4=read_log()
        electric_current.append(List1)
        Voltage.append(List2)
        TIME.append(List3)
        MOD.append(List4)

    ID=input("请输入ID：")
    time,elec,volt,date=extract(ID)
    PLOT_ELE(time,elec,date)
    print('end')