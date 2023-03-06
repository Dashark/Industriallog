import xlwt
import xlrd
import io
import pandas as pd
import numpy as np
import os
import xlrd
from xlutils.copy import copy
from datetime import datetime

import requests
path = 'E:/Industey-log-data/XFlogback-220526/Log/'
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
    print('请求url：', r.url)
    print('状态码：', r.status_code)
    print('文本响应内容：', r.text)


def load_date(fname):
    date1 = datetime(1970, 1, 1, 0, 0, 0)   # 初始一个古老时间
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as file:
            content1 = file.readline()   # 从文件中读取存储的时间
            date1 = datetime.strptime(content1, "%Y-%m-%d %H:%M:%S")
    return date1

if __name__ == '__main__':
    PATH = '/opt/data/' # docker中映射的目录
    timebuf_file = PATH + op + 'time_temp_log.txt'
    latest_date = load_date(timebuf_file)
    max_date = latest_date
    file_date = latest_date
    # 文件列表
    files = []
    files_name=[]
    if os.path.exists(PATH + op):
        for file in os.listdir(PATH + op):   # 看起来缺省上正确排序，不知道未来有没有问题
            if file.endswith(".log"):
                files.append(PATH + op + file)
                files_name.append(file)
    else:
        print(PATH, "doesn't exist. Check docker dir map !")
    for file in files:
        #fileaddress = 'E:/Industey-log-data/MSPS/Log/log_Data_1.xls'
        # TODO 缺少文件时间处理
        read_log(file)
        print('end')