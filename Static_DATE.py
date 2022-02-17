import xlrd  # 导入库
# 打开文件
xlsx = xlrd.open_workbook('E:\Hudasha\MSPS\Log\State.xls')
sheet1 = xlsx.sheets()[0]
nrows=sheet1.nrows
List = [[] for i in range(86)]
n=0
Date = sheet1.row(0)[0].value
for i in range(nrows):
    if Date==sheet1.row(i)[0].value:
        List[n].append(sheet1.row(i)[1].value)
    else:
        n=n+1
        List[n].append(sheet1.row(i)[1].value)
        Date=sheet1.row(i)[0].value
with open('E:\Hudasha\MSPS\Log\State.txt','w') as f:
    for i in List:
        for j in i:
            f.write(j)
            f.write(',')
        f.write('\n')
    f.close()
