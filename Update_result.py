import xlwt
import xlrd
import io
import pandas as pd
import numpy as np
import os
import xlrd
from xlutils.copy import copy

import requests
path = 'E:/Industey-log-data/XFlogback-220526/Log/'
def read_log():
    #f = xlwt.Workbook()
    # f = xlrd.open_workbook(fileaddress)
    # sheets = f.sheet_names()
    # worksheet = f.sheet_by_name(sheets[0])
    #sheet1 = f.add_sheet('log1')
    log = open(fileaddresstlog, 'r')
    # new_workbook = copy(f)  # 将xlrd对象拷贝转化为xlwt对象
    # rows_old = worksheet.nrows
    # new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    #exclbegin=
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

# def write_excel(r, table, sheet1):
#     print(r)
#     # f = xlwt.Workbook()
#     #   sheet1=f.add_sheet('log')
#     if table == 0:
#         row0 = ['key', 'value']
#     else:
#         row0 = table
#     for i in range(0, len(row0)):
#         sheet1.write(r, i, row0[i])


# 文件列表
files = []
for file in os.listdir(path):
    if file.endswith(".log"):
        files.append(path + file)

# 定义一个空的dataframe
data = pd.DataFrame()

# 遍历所有文件

    # datai = pd.read_csv(file, encoding='gbk')
    # datai_len = len(datai)
    # data = data.append(datai)  # 添加到总的数据中
    # print('读取%i行数据,合并后文件%i列, 名称：%s' % (datai_len, len(data.columns), file.split('/')[-1]))

if __name__ == '__main__':
    for fileaddresstlog in files:
        #fileaddress = 'E:/Industey-log-data/MSPS/Log/log_Data_1.xls'
        read_log()
        print('end')