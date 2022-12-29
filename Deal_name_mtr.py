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
def read_log(file):
    list1={}
    list3=[]
    log = open(file, 'r', encoding='gbk')  # Window系统中文编码是GBK的
    count=0
    for logline in log:
        if count<5:
            logline1=logline.split(':')
            list1[logline1[0]]=logline1[1].strip('/n')
        elif count>5:
            logline = logline.split('	')
            list2 = []
            for i in range(0,9):  # 标准切割出9份
                if i<len(logline):  # 实际上存在不足
                    list2.append(logline[i])
                else:
                    list2.append('*') # 不足部分补任意值
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
    response = urllib.request.urlopen(request, timeout=5)
    print(response.read().decode('utf-8'))
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
def load_date(fname):
    date1 = datetime(1970, 1, 1, 0, 0, 0)   # 初始一个古老时间
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as file:
            content1 = file.readline()   # 从文件中读取存储的时间
            date1 = datetime.strptime(content1, "%Y-%m-%d %H:%M:%S")
    return date1

def upload_subdir(op):
    PATH = '/opt/data/' # docker中映射的目录
    timebuf_file = PATH + op + 'time_temp_mtr.txt'
    latest_date = load_date(timebuf_file)
    max_date = latest_date
    # 文件列表
    files = []
    files_name=[]
    if os.path.exists(PATH + op):
        for file in os.listdir(PATH + op):   # 看起来缺省上正确排序，不知道未来有没有问题
            if file.endswith(".mtr"):
                files.append(PATH + op + file)
                files_name.append(file)
    else:
        print(PATH, "doesn't exist. Check docker dir map !")
    # print(files_name)
    for i, file in enumerate(files):
        filename = files_name[i]
        file_date = datetime.strptime(filename[4:19], '%Y%m%d_%H%M%S')
        if file_date > latest_date:  # 新时间文件可以上传
            List1,List2=read_log(file)
            Fin_MOD=Formulate(List1,List2)
            try:
                Update_gdf_json(Fin_MOD)
            except Exception as e:
                print(e)
                break
            if file_date > max_date:
                max_date = file_date
    with open(timebuf_file, 'w', encoding='utf-8') as file:
        file.write(max_date.strftime("%Y-%m-%d %H:%M:%S"))
    # ID=input("请输入ID：")
    # time,elec,volt,date=extract(ID)
    # PLOT_ELE(time,elec,date)
    # print('end')
if __name__ == '__main__':
    OP = ['检验功能/', '功能测试/', '高压测试/', '不合格项/']
    for op in OP:
        upload_subdir(op)