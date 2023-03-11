import numpy as np
import os
import json
import urllib.request
import urllib.error
from datetime import datetime

import requests
def read_log(file):
    log = open(file, 'r', encoding='gbk')
    r = 0
    for logline in log:
        logline1=logline.replace('       ','&')
        logline1= logline1.replace(' ', '&')
        logline1= logline1.replace('：', '&')
        logline1 = logline1.replace('    ', '&')
        logline1 = logline1.replace('      ', '&')
        update(logline1)#excelbegin+#
        r = r + 1
    #new_workbook.save(fileaddress)
def update(params):
    url = 'http://182.92.66.252:8092/prod-api/smart/threePart/insertString/'

    # 调用get
    r = requests.get(url+params)    # 响应对象
    print('请求url:', r.url)
    print('状态码:', r.status_code)
    print('文本响应内容:', r.text)


def load_date(fname):
    date1 = datetime(1970, 1, 1, 0, 0, 0)   # 初始一个古老时间
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as file:
            content1 = file.readline()   # 从文件中读取存储的时间
            date1 = datetime.strptime(content1, "%Y-%m-%d %H:%M:%S")
    return date1

if __name__ == '__main__':
    PATH = '/opt/data/' # docker中映射的目录
    timebuf_file = PATH + 'time_temp_log.txt'
    latest_date = load_date(timebuf_file)
    max_date = latest_date
    file_date = latest_date
    # 文件列表
    files = []
    files_name=[]
    if os.path.exists(PATH):
        for file in os.listdir(PATH):   # 看起来缺省上正确排序，不知道未来有没有问题
            if file.endswith(".log"):
                files.append(PATH + file)
                files_name.append(file)
    else:
        print(PATH, "doesn't exist. Check docker dir map !")
    for i, file in enumerate(files):
        filename = files_name[i]
        try:
            file_date = datetime.strptime(filename[0:15], '%Y%m%d_%H%M%S')
        except ValueError as ve:
            print('ValueError Raised: ', ve)
            continue
        if file_date > latest_date:  # 新时间文件可以上传
            try:
                read_log(file)
            except urllib.error.URLError as ue:
                print('URLError Raised: ', ue)
                break
            if file_date > max_date:
                max_date = file_date
    with open(timebuf_file, 'w', encoding='utf-8') as file:
        file.write(max_date.strftime("%Y-%m-%d %H:%M:%S"))
    print('end')