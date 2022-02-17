import xlwt
import xlrd
import io
import pandas as pd
import numpy as np
import os
import xlrd
from xlutils.copy import copy


path = 'C:/Users/Lenovo/Desktop/MSPS/Log/'
def read_log(route):
    #f = xlwt.Workbook()
    #sheet1 = f.add_sheet('log1')
    log = open(fileaddresstlog, 'r')
    #r = 1
    loglist=[]
    for logline in log:
        logline = logline.split('：')
        loglist.append(logline)
    write_excel(route, loglist)




files = []

def write_excel(route,value):
    index=len(value)
    workbook = xlrd.open_workbook(route)  # 打开工作簿
    sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
    worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
    rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
    new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
    new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
    for i in range(0, index):
        for j in range(0, len(value[i])):
            new_worksheet.write(i + rows_old, j, value[i])  # 追加写入数据，注意是从i+rows_old行开始写入
    new_workbook.save(route)  # 保存工作簿
    print("xls格式表格【追加】写入数据成功！")



def write_excel1(r, table, sheet1):
    print(r)
    # f = xlwt.Workbook()
    #   sheet1=f.add_sheet('log')
    if table == 0:
        row0 = ['key', 'value']
    else:
        row0 = table
    for i in range(0, len(row0)):
        sheet1.write(r, i, row0[i])
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
        fileaddress = 'C:/Users/Lenovo/Desktop/MSPS/Log/log_Data.xls'
        read_log(fileaddress)
        print('end')