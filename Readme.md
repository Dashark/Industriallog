1.先是处理原始的log文件

用rang_file.py进行处理，需要修改的是日志文件存储的文件夹以及输出的Excel表（例子中输出到了log_Data_1.xlsx中）（第11行要修改为日志所存储的文件夹；第66行修改为要输出的空excel）

2.将状态转化为字母表示形式

通过Stata_Change.py文件进行转化(ps：这个py文件本来是没有的，之前是直接用Exccel处理一个个替换的)（可以不替换）

3.频繁模式挖掘

之前记错了，prefixspan只能找到频繁模式，但没进行数量统计，后面使用的是Apriori算法做的，使用的是Apriori_test.py文件处理。但是在使用之前需要（可以用简单的数据进行一下测试）

​	1.在excel里通过单元格格式将01/01/2021改成2021-01-01这种形式（ps:log_Data->log_Data2就是这个改变）

​	2.处了修改文件，还要修改py文件中DAY这个变量，修改成实际的天数（第96行有这个变量定义）

最后输出结果是state.txt

4.截取reset之间的函数

​	1.修改了range_file加入了分秒到输出文件log_Data_1里面

​	2.通过修改between_reset.py中的log_Data_1的地址，即可运行，但由于边界问题，第一个dev_reset之前的状态未被存入txt中，最后一组dev_reset的状态也未被存入

