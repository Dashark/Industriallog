import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#标准曲线
#x =  np.linspace(0, 1, 100)
#t =  np.sin(2 * np.pi * x)
#采样函数
def get_data(fileaddress):
    data =pd.read_csv(fileaddress)
    x_n=data[['B']]
    t_n = data[['A']]
    return x_n, t_n
#绘制部分组件函数
def draw_ticks():
    plt.tick_params(labelsize=15)
    plt.xticks(np.linspace(400, 700))
    plt.yticks(np.linspace(800, 900))
    #plt.ylim(-1.5, 1.5)
    font = {'family':'Times New Roman','size':20}
    plt.xlabel('x', font)
    plt.ylabel('t',font, rotation='horizontal')
#采样
address='C:/Users/Lenovo/Desktop/0915test1.csv'
x_n, t_n = get_data(address)
x_3=np.array(x_n)
x_2=x_3.flatten()
t_n=np.array(t_n)
t_3=np.array(t_n)
t_2=t_3.flatten()
#图像绘制部分
# plt.figure(1, figsize=(8,5))
# #plt.plot(x, t, 'g',linewidth=3)
# plt.scatter(x_2, t_2, color='g', marker='o', edgecolors='b', s=100, linewidth=3, label="training data")
# draw_ticks()
# plt.title('Figure 1 : sample curve')
# plt.show()
#plt.savefig('1.png', dpi=400)
#拟合函数（lamda默认为0，即无正则项）
def chae(Y1,Y2):
    delete=[]
    for i in range(len(Y1)):
        delete.append(Y1[i]-Y2[i])
    VAR=np.var(delete)
    print(VAR)

x_2=np.array(x_2)
t_2=np.array(t_2)

fig,ax = plt.subplots()
# 二次拟合
coef = np.polyfit(x_2, t_2, 2)
y_fit = np.polyval(coef, x_2)
chae(y_fit,t_2)
ax.plot(x_2,y_fit,'r')
ax.plot(x_2, t_2, 'g')
plt.show()

# 找出其中的峰值/对称点
# if coef[0] != 0:
#     x0 = -0.5 * coef[1] / coef[0]
#     x0 = round(x0, 2)
#     ax.plot([x0]*5, np.linspace(min(y),max(y),5),'r--')
#     print(x0)
# else:
#     raise ValueError('Fail to fit.')


