import pandas as pd
import numpy as np
import couchdb
import os
import json
import urllib.request
import matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
import sys,os


from matplotlib import style
import requests
Function=[]
Voltage=[]
TIME=[]
MOD=[]
path = 'E:/Industey-log-data/name/Desktop/Log7月21-9月22日/'#可以把测试样例下载下来改成时间文件夹前面的地址
def read_log():
    list1=[]
    log = open(fileaddresstlog, 'r')
    for logline in log:
        logline=logline.replace('       ','&')
        logline= logline.replace(' ', '&')
        logline= logline.replace('：', '&')
        logline = logline.replace('    ', '&')
        logline = logline.replace('      ', '&')
        logline = logline.replace('         ', '&')
        logline = logline.replace('&&&&&&&', '&')
        logline = logline.replace('&&&&&&', '&')
        logline = logline.replace('&&&&', '&')
        logline = logline.replace('&&&', '&')
        logline = logline.replace('&&', '&')
        data1={}
        logline1 = logline.split('&')
        data1.setdefault('Date', logline1[0])
        data1.setdefault('Time',logline1[1])
        data1.setdefault('Func', logline1[2])
        data1.setdefault('Result',logline1[3])
        for i in range(len(logline1)-4):
            data1.setdefault('para'+str(i+1),logline1[i+4])
        list1.append(data1)
    return list1

# 文件列表
files = []
files_name=[]

for file in os.listdir(path):
    if file.endswith(".log"):
            files.append(path + file)
            files_name.append(file)
    else:
        for file1 in os.listdir(path+file+'/'):
            if file1.endswith(".log"):
                files.append(path + file+'/' +file1)
                files_name.append(file)
def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]#obj可以是字符串或队列
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
# def PLOT_ELE(time1,elec1,date):
#     for r in range(len(time1)):
#         #new_electric_current=unified_dimension_Y(elec1[r])
#         #time=float(date)+float(time1)
#         time2=[]
#         for i in range(len(time1[r])):
#             x=float(time[r][i])+float(date[r])
#             time2.append(x)
#         plt.plot(time2, elec1[r])
#     plt.show()
# def extract(id_no):
#     temp_time=[]
#     temp_elec=[]
#     temp_volt=[]
#     temp_datetime=[]
#     for i in range(len(TIME)):
#         str_id=str(MOD[i][1].values()).strip('dict_values([\'')
#         str_id=str_id.replace("\\n\'])",'')
#         if id_no==str_id:
#             str_date = str(MOD[i][4].values()).strip('dict_values([\'')
#             str_date = str_date.replace("\\n\'])", '')
#             temp_datetime.append(str_date)
#             temp_time.append(TIME[i])
#             temp_elec.append(Function[i])
#             temp_volt.append(Voltage[i])
#     return temp_time,temp_elec,temp_volt,temp_datetime
def Update_gdf_json(data):
    #url = 'http://182.92.66.252:8092/prod-api/smart/threePart/insertTesting'
    # 调用get    #r = requests.get(url + params)  # 响应对象
    headers={'Content-Type':'application/json'}
    request  = urllib.request.Request(url='http://182.92.66.252:8092/prod-api/smart/threePart/insertTesting/', headers=headers,data=json.dumps(data).encode('utf-8'))
    response = urllib.request.urlopen(request)
    print(response)
    print('状态码：',response.getcode())
def Update_gdf_CouchDB(file):
    couch = couchdb.Server("http://fxz_admin:fxz123456@47.96.146.116:5984/")
    document_gdf=json.dumps(file)
    db=couch['log_2']#['gdf']#['gdf'] # 新建数据库
    #db= {'data': document_gdf}
    document_gdf= json.loads(document_gdf)
    db.save(document_gdf)
    print(document_gdf)
def Formulate(first_list):
    Dict={}
    Dict.setdefault('type','log')
    Dict.setdefault('ModFunc',first_list)
    return Dict
def Write_Pointrow(filename,num,str):
    Filename = open(filename, 'r+')
    flist = Filename.readlines()
    flist[num] = str
    f = open(filename, 'w+')
    f.writelines(flist)


def judge_new_or_nor(Name):
    if_new = 0
    year = cut(Name,15)
    with open('E:/Industey-log-data/name/Desktop/time_temp.txt', encoding='utf-8') as file:
        content1 = file.read()
        content1.rstrip()
    content = content1.split('\n')
    new_year = content[0]
    new_month = content[1]
    new_day = content[2]
    new_hour = content[3]
    new_minute = content[4]
    new_second = content[5]
    DATE = datetime.strptime(year[0], '%Y%m%d_%H%M%S')
    if DATE.year > int(new_year):
        new_year = str(DATE.year)+'\n'
        Write_Pointrow('E:/Industey-log-data/name/Desktop/time_temp.txt',0,new_year)
        if_new = 1
    if DATE.month > int(new_month):
        new_month = str(DATE.month)+'\n'
        Write_Pointrow('E:/Industey-log-data/name/Desktop/time_temp.txt', 1, new_month)
        if_new = 1
    if  DATE.day > int(new_day):
        new_day = str(DATE.day)+'\n'
        Write_Pointrow('E:/Industey-log-data/name/Desktop/time_temp.txt', 2, new_day)
        if_new = 1
    if  DATE.hour > int(new_hour):
        new_hour = str(DATE.hour)+'\n'
        Write_Pointrow('E:/Industey-log-data/name/Desktop/time_temp.txt', 3, new_hour)
        if_new = 1
    if  DATE.minute > int(new_minute):
        new_minute = str(DATE.minute)+'\n'
        Write_Pointrow('E:/Industey-log-data/name/Desktop/time_temp.txt', 4, new_minute)
        if_new = 1
    if int(DATE.second) > int(new_second):
        new_second=str(DATE.second)+'\n'
        Write_Pointrow('E:/Industey-log-data/name/Desktop/time_temp.txt', 5, new_second)
        if_new = 1
    if if_new == 1:
        if_new=0
        return 1
    else:
        return 0
if __name__ == '__main__':
    r=0
    for i in range(len(files)):
        fileaddresstlog=files[i]
        filename=files_name[i]
        if judge_new_or_nor(filename)==1:
            List1=read_log()
            Function.append(List1)
    for i in range(len(Function)):
        Fin_MOD=Formulate(Function[i])
       # print(files[i])
        Update_gdf_CouchDB(Fin_MOD)
    # ID=input("请输入ID：")
    # time,elec,volt,date=extract(ID)
    # PLOT_ELE(time,elec,date)
    # print('end')