#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import xlrd
import xlwt

list=[]
def handler_excel(filename=r'E:/Industey-log-data/Industriallog/log_Data_1.xlsx'):
    # 打开文件
    workbook = xlrd.open_workbook(filename)
    index = workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name(index)

    # 遍历
    i=0
    count = 0
    nrows = sheet.nrows
    while i < nrows:
        value=sheet.cell_value(i,2)
        if value=='Dev_Reset':
            Name1=str(sheet.cell_value(i,1)+sheet.cell_value(i,0))
            Name = Name1.replace(":", ".")  # 删除隐藏的字符\ufeff
            while i< nrows:
                list.append(sheet.row_values(i))
                value1=sheet.cell_value(i+1,2)
                if value1=='Dev_Reset' :
                    i=i+1
                    write_txt(Name+'.txt',list)
                    list.clear()
                    count=count+1
                    break
                else:
                    i=i+1
        else:
            i=i+1


def write_excel(filename,list1):
    f = xlwt.Workbook('encoding = utf-8') #设置工作簿编码
    sheet1 = f.add_sheet('sheet1',cell_overwrite_ok=True) #创建sheet工作表
    for i in range(len(list1)):
        sheet1.write(i,0,list1[i]) #写入数据参数对应 行, 列, 值
    f.save(filename)#保存.xls到当前工作目录
def write_txt(filename,list1):
    file_handle=open(filename,mode='w')
    for i in range(len(list1)):
        file_handle.write(str(list1[i])+'\n')#写入数据参数对应 行, 列, 值
    #file_handle.save(filename)#保存.xls到当前工作目录


if __name__ == '__main__':
    handler_excel()