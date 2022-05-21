import xlrd
import pandas as pd
import  numpy as np
# coding:utf-8
import itertools


class Apriori:
    def __init__(self, min_sup=0.2, dataDic={}):
        self.data = dataDic
        self.size = len(dataDic)  # Get the number of events
        self.min_sup = min_sup
        self.min_sup_val = 1#min_sup * self.size  # 这个数值是频繁算法的分子整数部分

    def find_frequent_1_itemsets(self):
        FreqDic = {}  # {itemset1:freq1,itemsets2:freq2}  不管频繁度如何，先计算频繁度，然后装到这里面
        for event in self.data:  # event表示字典里的键值，比如T100
            for item in self.data[event]:
                if item in FreqDic:  # 该成员是否出现过，出没出现过都要对它进行赋值
                    FreqDic[item] += 1  # 出现过则+1
                else:
                    FreqDic[item] = 1  # 没出现过则初始值为1
        L1 = []
        L1_freq=[]
        for itemset in FreqDic:  # 遍历第一轮“频繁”的成员
            if FreqDic[itemset] >= self.min_sup_val:  # 如果频繁度大于设定值
                L1.append([itemset])  # 将该成员推入列表,仅仅是将成员推入列表，频度不管
                L1_freq.append(FreqDic[itemset])
        return L1,L1_freq

    def has_infrequent_subset(self, c, L_last, k):  # 这是一个进行排列组合的函数
        subsets = list(itertools.combinations(c, k - 1))  # 在列表c中选择k-1个元素进行无序组合
        for each in subsets:  # 遍历这些组合的情况
            each = list(each)  # 把元素强制转换成列表
            if each not in L_last:  # 如果上一轮筛选出的集合中的成员没有在该组合中出现，则返回一个True，出现过则继续遍历所有组合的情况
                return True
        return False

    def apriori_gen(self, L_last):  # L_last means frequent(k-1) itemsets 难点！！！
        k = len(L_last[0]) + 1  # len()对于列表，则返回成员的个数 如['I1','I2']就返回2
        Ck = []  # 候选项集集合
        for itemset1 in L_last:  # 循环遍历L_last中的成员
            for itemset2 in L_last:
                # join step
                flag = 0
                for i in range(k - 2):
                    if itemset1[i] != itemset2[i]:
                        flag = 1  # the two itemset can't join
                        break
                if flag == 1:
                    continue
                if itemset1[k - 2] < itemset2[k - 2]:
                    c = itemset1 + [itemset2[k - 2]]  # 例：['I1']<['I2']成立，则推入一个['I1','I2']，并且先不计算它的频繁度
                else:
                    continue
                    # pruning setp
                if self.has_infrequent_subset(c, L_last, k):
                    continue
                else:
                    Ck.append(c)  # 候选项集集合,还没有计算频繁度，先把各种组合扔进去
        return Ck

    def do(self):
        L_last,L_last_freq = self.find_frequent_1_itemsets()
        L = L_last
        i = 0
        while L_last != []:  # 只要本组频繁项集不空则继续循环
            Ck = self.apriori_gen(L_last)  # 候选项集集合(仅仅是各种排列组合，没筛选频繁度)推入Ck中
            FreqDic = {}
            for event in self.data:  # 遍历原始Data数据
                # get all suported subsets
                for c in Ck:  # 遍历候选的所有项集集合
                    if set(c) <= set(self.data[event]):  # set()表示无序不重复元素集,如果c元素集是原始数据这个集合的子集
                        if tuple(c) in FreqDic:  # 如果元组c在字典中
                            FreqDic[tuple(c)] += 1  # 这个元组的值+1，即又出现了一次
                        else:
                            FreqDic[tuple(c)] = 1
            print(FreqDic) # 将候选项集集合，以及出现的次数，以字典的形式打印出来，到这里时仍然没计算频繁度
            Lk = []  # 满足频繁度集合的列表
            Lk_freq=[]
            for c in FreqDic:  # 遍历字典里的所有候选集合
                #emp=[]
                if FreqDic[c] > self.min_sup_val:  # 如果大于设定的频繁度
                 #   temp=list(c).copy()
                  #  temp.append(str(+FreqDic[c]))
                  #  Lk.append(temp)  # 将该列表推入列表Lk中
                    Lk.append(list(c))
                    Lk_freq.append(FreqDic[c])
            L_last = Lk  # 将该列表定义为满足频繁度的最后一组列表
            L += Lk  # 最终结果的列表为L
            L_last_freq+=Lk_freq
        return L, L_last_freq
xlsx = xlrd.open_workbook('E:\Industey-log-data\MSPS\Log\State.xls')
sheet1 = xlsx.sheets()[0]
nrows=sheet1.nrows
List = [[] for i in range(86)]
n=0
Date_list=[]
Date = sheet1.row(0)[0].value
Date_list.append(Date)
for i in range(nrows):
    if Date==sheet1.row(i)[0].value:
        List[n].append(sheet1.row(i)[1].value)
    else:
        n=n+1
        List[n].append(sheet1.row(i)[1].value)
        Date=sheet1.row(i)[0].value
        Date_list.append(Date)

#data = pd.DataFrame({str(Date_list[0]): List[0]})
dict={}
for i in range(86):
     dict[str(Date_list[i])] = List[i]
a= Apriori(dataDic=dict)
Index,Frequency=a.do()
Dictionary={}
for i in range(len(Index)):
    Dictionary[str(Index[i])]=Frequency[i]
# print (d.do())

with open('E:\Industey-log-data\MSPS\Log\State_Frequency2.txt','w') as f:
    for i in range(len(Index)):
        for j in Index[i]:
            f.write(j)
            f.write(',')
        f.write(':')
        f.write(str(Frequency[i]))
        f.write('\n')
    f.close()
