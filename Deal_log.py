import pandas as pd
import numpy as np
import couchdb
import os
import json
import urllib.request
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import requests
Function=[]
Voltage=[]
TIME=[]
MOD=[]
path = 'E:/Industey-log-data/XFlogback-220526/Log/'#可以把测试样例下载下来改成时间文件夹前面的地址
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
for file in os.listdir(path):
    if file.endswith(".log"):
            files.append(path + file)
    else:
        for file1 in os.listdir(path+file+'/'):
            if file1.endswith(".log"):
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
    db=couch['log']#['gdf']#['gdf'] # 新建数据库
    #db= {'data': document_gdf}
    document_gdf= json.loads(document_gdf)
    db.save(document_gdf)
    print(document_gdf)
def Formulate(first_list):
    Dict={}
    Dict.setdefault('type','log')
    Dict.setdefault('ModFunc',first_list)
    return Dict
if __name__ == '__main__':
    r=0
    for fileaddresstlog in files:
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