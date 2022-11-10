import pandas as pd
import couchdb
import numpy as np
import os
import json
import urllib.request
import matplotlib
import matplotlib.pyplot as plt

path_log = 'E:/Industey-log-data/name/Desktop/Log7月21-9月22日/'
path_mtr = 'E:/Industey-log-data/name/Desktop/高压测试/'
files_log = []
files_mtr=[]
files_gdf=[]
for file in os.listdir(path_log):
    files_log.append(file)
for file in os.listdir(path_mtr):
    if file.endswith(".gdf"):
        files_gdf.append(file)
    else:
        files_mtr.append(file)
now_day=[1]
now_year=[1]
now_month=[1]
now_hour=[1]
now_minutes=[1]
now_seconds=[1]
def cut(obj, sec):
    return [obj[i:i+sec] for i in range(0,len(obj),sec)]#obj可以是字符串或队列
if_new=0
for fileaddresstlog in range(len(files_log)):
    year=cut(fileaddresstlog, 4)
    if int(year[0])>int(now_year[0]):
        now_year[0]=year[0]
        if_new=1
    month_and_day=cut(year[1],2)
    if int(month_and_day[0])>int(now_month[0]):
        now_month[0]=month_and_day[0]
        if_new = 1
    if int(month_and_day[1]) > int(now_day[0]):
        now_day[0]=month_and_day[1]
        if_new = 1
    hour=cut(fileaddresstlog,9)
    time=cut(hour,2)
    if int(time[0]) > int(now_hour[0]):
        now_hour[0]=time[0]
        if_new = 1
    if int(time[1]) > int(now_minutes[0]):
        now_hour[0] = time[1]
        if_new = 1
    if int(time[2]) > int(now_seconds[2]):
        now_seconds.append(int(time[2]))
        if_new = 1
    if if_new==1:
       ....

