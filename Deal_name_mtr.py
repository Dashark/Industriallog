import pandas as pd
import couchdb
import numpy as np
import os
import json
import urllib.request
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import requests
path = '.'#可以把测试样例下载下来改成时间文件夹前面的地址
def read_log(file):
    list1={}
    list3=[]
    log = open(file, 'r')
    count=0
    for logline in log:
        data1={}
        if count<5:
            logline1=logline.split(':')
            list1[logline1[0]]=logline1[1].strip('/n')
        elif count>5:
            logline = logline.split('	')
            list2 = []
            for i in range(0,9):
                if i<len(logline):
                    list2.append(logline[i])
                else:
                    list2.append(' ')
            list3.append(list2)
        count=count+1
    return list1,list3#代表时间、电流、电压、Mod

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
def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]
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
    Dict.setdefault('ModStr', first_list)
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
    Dict.setdefault('ModList',data_list)

    return Dict
    """
    1. 一次性把文件名cut出来形成['高压测试','20220207_084509']
    2. 使用Python库的datetime的strptime函数直接转换时间
    3. 最新的时间要存盘的, 程序初始化从文件中得到时间(now_year这个变量)
    4. 2个datetime可以直接比较的
    """
if __name__ == '__main__':
    r=0
    latest_date = datetime(1970, 1, 1, 0, 0, 0)   # 初始一个古老时间
    max_date = datetime(1970, 1, 1, 0, 0, 0)   # 初始一个古老时间
    if os.path.exists('time_temp_mtr.txt'):
        with open('time_temp_mtr.txt', 'r', encoding='utf-8') as file:
            content1 = file.readline()   # 从文件中读取存储的时间
            latest_date = datetime.strptime(content1, "%Y-%m-%d %H:%M:%S")
    # 文件列表
    files = []
    files_name=[]
    for file in os.listdir(path):
        if file.endswith(".mtr"):
            files.append(path + file)
            files_name.append(file)
    for i in range(len(files)):
        filename = files_name[i]
        file_date = datetime.strptime(filename[4:19], '%Y%m%d_%H%M%S')
        if file_date > latest_date:  # 新时间文件可以上传
            List1,List2=read_log(files[i])
            Fin_MOD=Formulate(List1,List2)
            Update_gdf_json(Fin_MOD)
            if file_date > max_date:
                max_date = file_date
    with open('time_temp_mtr.txt', 'w', encoding='utf-8') as file:
        file.write(max_date.strftime("%Y-%m-%d %H:%M:%S"))
    # ID=input("请输入ID：")
    # time,elec,volt,date=extract(ID)
    # PLOT_ELE(time,elec,date)
    # print('end')