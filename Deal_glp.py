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
MODLIST=[]
MODSTR=[]
path = 'E:/Industey-log-data/XFlogback-220526/PlotData/'#可以把测试样例下载下来改成时间文件夹前面的地址
def read_log():
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    log = open(fileaddresstlog, 'r')
    count=0
    for logline in log:
        data1={}
        data2={}
        if count>0 and logline[0]=='M':
            logline1=logline.replace('->','&')
            logline1 = logline1.replace('	', '&')
            logline1 = logline1.replace(':', '&')
            logline1=logline1.split('&')
            if logline1[0]=='ModList':
                data1[logline1[1]]=logline1[2].replace('\n',' ')
                list4.append(data1)
            elif logline1[0]=='ModStr':
                data2[logline1[1]]=logline1[2]
                data2[logline1[4]]=logline1[5]
                data2[logline1[7]]=logline1[8]
                list5.append(data2)
        elif count>0:
            logline = logline.split('	')
            list1.append(logline[2])
            list2.append(logline[1])
            list3.append(logline[0])
        count=count+1
    return list1,list2,list3,list4,list5#代表时间、电流、电压、Mod

# 文件列表
files = []
for file in os.listdir(path):
    if os.path.isfile(file):
        if file.endswith(".glp"):
            files.append(path + file)
    else:
        for file1 in os.listdir(path+file+'/'):
            if file1.endswith(".glp"):
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

# def PLOT_Vol():
#     for r in range(len(TIME)):
#         # electric_current[r]=electric_current[r]/sum(electric_current[r])
#         new_Voltage = unified_dimension_Y(Voltage[r])
#         plt.plot(TIME[r], new_Voltage)
#     plt.show()
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
#             temp_elec.append(electric_current[i])
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
    db=couch['glp']#['gdf']#['gdf'] # 新建数据库
    #db= {'data': document_gdf}
    document_gdf= json.loads(document_gdf)
    db.save(document_gdf)
    print(document_gdf)
def Formulate(first_list,second_list,third_list,forth_list,fifth_list):
    Dict={}
    Dict.setdefault('type','glp')
    data_list=[]
    for i in range(len(first_list)):
        data_dict={}
        data_dict.setdefault('time',third_list[i])
        data_dict.setdefault('current',second_list[i])
        data_dict.setdefault('voltage',first_list[i])
        data_list.append(data_dict)
    Dict.setdefault('data',data_list)
    Dict.setdefault('ModStr',fifth_list)
    Dict.setdefault('ModList',forth_list)
    return Dict
if __name__ == '__main__':
    r=0
    for fileaddresstlog in files:
        List1,List2,List3,List4,List5=read_log()
        electric_current.append(List1)
        Voltage.append(List2)
        TIME.append(List3)
        MODLIST.append(List4)
        MODSTR.append(List5)
    for i in range(len(MODLIST)):
        Fin_MOD=Formulate(electric_current[i],Voltage[i],TIME[i],MODLIST[i],MODSTR[i])
        print(files[i])
        Update_gdf_json(Fin_MOD)
        #Update_gdf_CouchDB(Fin_MOD)
    # ID=input("请输入ID：")
    # time,elec,volt,date=extract(ID)
    # PLOT_ELE(time,elec,date)
    print('end')