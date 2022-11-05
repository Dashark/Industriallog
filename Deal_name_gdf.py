import pandas as pd
import couchdb
import numpy as np
import os
import json
import urllib.request
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import requests
electric_current=[]
Voltage=[]
TIME=[]
MOD=[]
path = 'E:/Industey-log-data/name/Desktop/高压测试/'#可以把测试样例下载下来改成时间文件夹前面的地址
def read_log():
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    log = open(fileaddresstlog, 'r')
    count=0
    for logline in log:
        data1={}
        if count<8:
            logline1=logline.split(':')
            logline2=logline1[0].split('->')
            data1[logline2[1]]=logline1[1].strip('/n')
            list4.append(data1)
        elif count>8:
            logline = logline.split('	')
            list1.append(logline[2])
            list2.append(logline[1])
            list3.append(logline[0])
        count=count+1
    return list1,list2,list3,list4#代表时间、电流、电压、Mod

# 文件列表
files = []
files_name=[]
now_day=[1]
now_year=[1]
now_month=[1]
now_hour=[1]
now_minutes=[1]
now_seconds=[1]
for file in os.listdir(path):
    if file.endswith(".gdf"):
            files.append(path + file)
            files_name.append(file)
    # else:
    #     for file1 in os.listdir(path+file+'/'):
    #         if file1.endswith(".gdf"):
    #             files.append(path + file+'/' +file1)
    #             files_name.append(file1)
data = pd.DataFrame()
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
    db=couch['function-test-gdf']#['gdf']#['gdf'] # 新建数据库
    #db= {'data': document_gdf}
    document_gdf= json.loads(document_gdf)
    db.save(document_gdf)
    print(document_gdf)
def Formulate(first_list,second_list,third_list,forth_list):
    Dict={}
    Dict.setdefault('type','gdf')
    data_list=[]
    for i in range(len(first_list)):
        data_dict={}
        data_dict.setdefault('time',third_list[i])
        data_dict.setdefault('current',second_list[i])
        data_dict.setdefault('voltage',first_list[i])
        data_list.append(data_dict)
    Dict.setdefault('data',data_list)
    Dict.setdefault('ModStr',forth_list)
    return Dict
def judge_new_or_nor(Name):
    if_new = 0
    year = cut(Name, 4)
    if int(year[1]) > int(now_year[0]):
        now_year[0] = year[1]
        if_new = 1
    month_and_day = cut(year[2], 2)
    if int(month_and_day[0]) > int(now_month[0]):
        now_month[0] = month_and_day[0]
        if_new = 1
    if int(month_and_day[1]) > int(now_day[0]):
        now_day[0] = month_and_day[1]
        if_new = 1
    hour = cut(Name, 13)
    time = cut(hour[1], 2)
    if int(time[0]) > int(now_hour[0]):
        now_hour[0] = time[0]
        if_new = 1
    if int(time[1]) > int(now_minutes[0]):
        now_hour[0] = time[1]
        if_new = 1
    if int(time[2]) > int(now_seconds[0]):
        now_seconds[0]=time[2]
        if_new = 1
    if if_new == 1:
        if_new=0
        return 1
    else:
        return 0
if __name__ == '__main__':
    r=0
    for i in range(len(files)):
        fileaddresstlog = files[i]
        filename = files_name[i]
        if judge_new_or_nor(filename) == 1:
            List1,List2,List3,List4=read_log()
            electric_current.append(List1)
            Voltage.append(List2)
            TIME.append(List3)
            MOD.append(List4)
    for i in range(len(MOD)):
        Fin_MOD=Formulate(electric_current[i],Voltage[i],TIME[i],MOD[i])
        Update_gdf_CouchDB(Fin_MOD)
    ID=input("请输入ID：")
    time,elec,volt,date=extract(ID)
    PLOT_ELE(time,elec,date)
    print('end')