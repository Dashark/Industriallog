import xlrd as xd
data =xd.open_workbook ('E:/Industey-log-data/Industriallog/log_Data_1.xlsx') #range_file的结果
sheet = data.sheet_by_name('Sheet1')  #读取数据，以excel表名来打开
List = []
for r in range(sheet.nrows): #将表中数据按行逐步添加到列表中，最后转换为list结构
    for c in range(2):
        List.append(sheet.cell_value(r,c))
list1 = ['A' if i == 'Dev_GetInfo' else i for i in List]
list1 = ['B' if i == 'Dev_Reset' else i for i in list1]
list1 = ['C' if i == 'Dev_ModPower' else i for i in list1]
list1 = ['D' if i == 'Mod_GetIdVer' else i for i in list1]
list1 = ['E' if i == 'Mod_NextCtrlOn' else i for i in list1]
list1 = ['F' if i == 'Dev_LEDCtrl' else i for i in list1]
list1 = ['G' if i == 'Mod_DetonCtrl30sH' else i for i in list1]
list1 = ['H' if i == 'Unknow' else i for i in list1]
list1 = ['I' if i == 'Mod_NextCtrlOff' else i for i in list1]
list1 = ['J' if i == 'Mod_DetonCtrl15s' else i for i in list1]
list1 = ['K' if i == 'Dev_KA23Ctrl' else i for i in list1]
list1 = ['L' if i == 'Dev_KA1Ctrl' else i for i in list1]
list1 = ['M' if i == 'Dev_KA4Ctrl' else i for i in list1]
list1 = ['N' if i == 'WARN_VoltCurr' else i for i in list1]
print(list1)
# 定义指定输出Excel文件的名称，读入方式，编码方式
result = open('log_Data.xlsx', 'w', encoding='gbk')
# 参数'w'表示往指定表格读入数据，会先将表格中原本的内容清空
# 若把参数’w'修改为‘a+',即可实现在原本内容的基础上，增加新写入的内容
count=0
for i in range(0, len(list1)):
    result.write(str(list1[i]))
    result.write('\t')  # '\t'表示每写入一个元素后，会移动到同行的下一个单元格
    count+=1
    if count==2:
        count=0
        result.write("\n")  # 换行操作
result.write("\n")  # 换行操作
result.close()
