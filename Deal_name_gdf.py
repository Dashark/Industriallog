import couchdb
import numpy as np
import os
import json
import urllib.request
import urllib.error
from datetime import datetime
def read_log(file):
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    log = open(file, 'r', encoding='gbk').encode('utf-8')  # Window系统中文编码是GBK的
    count=0
    for line in log:
        data1={}
        logline = line.encode('utf-8').decode('utf-8')
        if count<8:
            logline1=logline.split(':', 1)
            logline2=logline1[0].split('->', 1)
            data1[logline2[1]]=logline1[1].strip()
            list4.append(data1)
        elif count>8:
            logline = logline.split('\t')
            list1.append(logline[2].strip())
            list2.append(logline[1])
            list3.append(logline[0])
        count=count+1
    return list1,list2,list3,list4#代表时间、电流、电压、Mod

#     # else:
#     #     for file1 in os.listdir(path+file+'/'):
#     #         if file1.endswith(".mtr"):
#     #             files.append(path + file+'/' +file1)
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
    timebuf_file = PATH + op + 'time_temp_gdf.txt'
    latest_date = load_date(timebuf_file)
    max_date = latest_date
    file_date = latest_date
    # 文件列表
    files = []
    files_name=[]
    if os.path.exists(PATH + op):
        for file in os.listdir(PATH + op):   # 看起来缺省上正确排序，不知道未来有没有问题
            if file.endswith(".gdf"):
                files.append(PATH + op + file)
                files_name.append(file)
    else:
        print(PATH + op, "doesn't exist. Check docker dir map !")
        return
    # print(files_name)
    for i, file in enumerate(files):
        filename = files_name[i]
        try:
            if len(filename) <= 32:   # 正常文件名
                file_date = datetime.strptime(filename[4:19], '%Y%m%d_%H%M%S')
            else:
                file_date = datetime.strptime(filename[9:24], '%Y%m%d_%H%M%S')
        except ValueError as ve:
            print('ValueError Raised: ', ve)
            continue
        if file_date > latest_date:  # 新时间文件可以上传
            current, voltage, stamp, mod =read_log(file)
            mod.append({'测试项目':filename[0:4]})
            Fin_MOD=Formulate(current,voltage,stamp,mod)
            try:
                Update_gdf_json(Fin_MOD)
            except urllib.error.URLError as ue:
                print('URLError Raised: ', ue)
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
    OP = ['检验功能/', '功能测试/', '高压测试/', '不合格项/', '振动测试/','高温测试/', '烧写ID/']
    # OP = ['检验功能/', '功能测试/', '高压测试/', '不合格项/']
    for op in OP:
        upload_subdir(op)