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
Info=[]
Ave_ele_Current=[]
time=[]
ID=[]
CAP=[]
Ave_ele_Current=[]
Ave_volt=[]
Hig_ele_Current=[]
Hig_volt=[]
Conjection=[]
Result=[]
path = 'E:/Industey-log-data/数据/Data/高压测试/'#可以把测试样例下载下来改成时间文件夹前面的地址
def read_log():
    list1=[]

    list3=[]
    log = open(fileaddresstlog, 'r')
    count=0
    for logline in log:
        data1={}
        if count<5:
            logline1=logline.split(':')
            data1[logline1[0]]=logline1[1].strip('/n')
            list1.append(data1)
        elif count>5:
            logline = logline.split('	')
            list2 = []
            for i in range(0,9):
                if i<len(logline):
                    list2.append(logline[i])
                else:
                    list2.append(' ')
            list3.append(list2)
            # if len(logline)>=1:
            #     list2.append(logline[0])
            #     if len(logline)>=2:
            #         list3.append(logline[1])
            #         if len(logline) >= 3:
            #             list4.append(logline[2])
            #             if len(logline)>=4:
            #                 list5.append(logline[3])
            #                 if len(logline)>=5:
            #                     list6.append(logline[4])
            #                     if len(logline) >= 6:
            #                         list7.append(logline[5])
            #                         if len(logline) >= 7:
            #                             list8.append(logline[6])
            #                             if len(logline) >= 8:
            #                                 list9.append(logline[7])
            #                                 if len(logline) >= 9:
            #                                     list10.append(logline[8])
        count=count+1
#        , list3, list4, list5, list6, list7, list8, list9, list10, len(logline)
    return list1,list3#代表时间、电流、电压、Mod

# 文件列表
files = []
for file in os.listdir(path):
    if file.endswith(".mtr"):
            files.append(path + file)
#     # else:
#     #     for file1 in os.listdir(path+file+'/'):
#     #         if file1.endswith(".mtr"):
#     #             files.append(path + file+'/' +file1)
data = pd.DataFrame()
def unified_dimension_Y(List1):
    arr_sum=1
    newdata=[]
    for i in range(len(List1)):
        arr_sum=arr_sum+float(List1[i])
    for i in range(len(List1)):
        newdata.append(float(List1[i])/arr_sum)
    return newdata

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
    db=couch['high-voltage-mtr']#['gdf']#['gdf'] # 新建数据库
    #db= {'data': document_gdf}
    document_gdf= json.loads(document_gdf)
    db.save(document_gdf)
    print(document_gdf)
def Formulate(first_list,second_list):
    Dict={}
    Dict.setdefault('type','mtr')
    data_list=[]
    Dict.setdefault('Mtr_Info', first_list[0])
    i=0
    while i<len(second_list):
        data_dict={}
        data_dict.setdefault('time',second_list[i][0])
        # data_dict.setdefault('initial id', third_list[0][i])
        # data_dict.setdefault('input id', forth_list[0][i])
        # data_dict.setdefault('current', fifth_list[0][i])
        # data_dict.setdefault('voltage', sixth_list[0][i])
        # data_dict.setdefault('Result', seventh_list[0][i])
        data_dict.setdefault('switch id',second_list[i][1])
        data_dict.setdefault('cap',second_list[i][2])
        data_dict.setdefault('The average current', second_list[i][3])
        data_dict.setdefault('The average voltage', second_list[i][4])
        data_dict.setdefault('The highest current', second_list[i][5])
        data_dict.setdefault('The highest voltage', second_list[i][6])
        data_dict.setdefault('The Cascade current ',second_list[i][7])
        data_dict.setdefault('Result', second_list[i][8])
        data_list.append(data_dict)
        i=i+1
    Dict.setdefault('data',data_list)

    return Dict
if __name__ == '__main__':
    r=0
    for fileaddresstlog in files:
        List1,List2=read_log()
        # ID.append(List3)
        # CAP.append(List3)
        # Ave_ele_Current.append(List5)
        # Ave_volt.append(List6)
        # Hig_ele_Current.append(List7)
        # Hig_volt.append(List8)
        # Conjection.append(List9)
        # Result.append(List10)
    # for i in range(len(time)):
#        , ID, CAP, Ave_ele_Current, Ave_volt, Hig_ele_Current, Hig_volt, Conjection, Result, logline_length
        Fin_MOD=Formulate(List1,List2)
        #Update_gdf_CouchDB(Fin_MOD)
        Update_gdf_json(Fin_MOD)
    # ID=input("请输入ID：")
    # time,elec,volt,date=extract(ID)
    # PLOT_ELE(time,elec,date)
    # print('end')