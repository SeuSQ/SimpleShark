import matplotlib.pyplot as plt
import math
import numpy as np

def calc(data):
    n = len(data)
    niu = 0.0
    niu2 = 0.0
    niu3 = 0.0
    for a in data:
        niu += a
        niu2 += a**2
        niu3 += a**3
    niu/= n   #这是求E(X)
    niu2 /= n #这是E(X^2)
    niu3 /= n #这是E(X^3)
    sigma = math.sqrt(niu2 - niu*niu) #这是D（X）的开方，标准差
    return [niu,sigma,niu3] #返回[E（X）,标准差，E（X^3）]

def calc_stat(data):
    [niu,sigma,niu3] = calc(data)
    n = len(data)
    niu4 = 0.0
    for a in data:
        a -= niu
        niu4 += a ** 4
    niu4 /= n
    skew = (niu3 - 3*niu*sigma**2 - niu**3)/(sigma**3)
    kurt =  niu4/(sigma**2)
    return [niu,sigma,skew,kurt] #返回了均值，标准差，偏度，峰度

if __name__== "__main__":
    data = list(np.random.randn(10000))#关于此处的数组与列表
    data2 = list(2*np.random.randn(10000))
    data3 = [x for x in data if x> -0.5]
    data4 = list(np.random.uniform(0,4,10000))
    [niu,sigma,skew,kurt] = calc_stat(data)
    [niu2,sigma2,skew2,kurt2] = calc_stat(data2)
    [niu3,sigma3,skew3,kurt3] = calc_stat(data3)
    [niu4,sigma4,skew4,kurt4] = calc_stat(data4)
    print (niu,sigma,skew,kurt)
    print (niu2,sigma2,skew2,kurt2)
    print (niu3,sigma3,skew3,kurt3)
    print (niu4,sigma4,skew4,kurt4)

    info = r'$\mu=%.2f,\ \sigma=%.2f,\ skew=%.2f,\ kurt=%.2f$'%(niu,sigma,skew,kurt)
    info2 =r'$\mu=%.2f,\ \sigma=%.2f,\ skew=%.2f,\ kurt=%.2f$'%(niu2,sigma2,skew2,kurt2)
    plt.text(1,0.38,info,bbox=dict(facecolor='red',alpha=0.25))
    plt.text(1,0.35,info2,bbox=dict(facecolor='green',alpha=0.25))
    #plt.text(x的位置，y的位置，面板内写的信息，标签框的属性=dict（facecolor='面板颜色'，alpha='深浅度'）)
    plt.hist(data,50,normed=True,facecolor='r',alpha=0.9)
    #hist直方图/箱式图(
    #将data中的元素分到50个等间隔的范围内，返回每个范围内元素的个数作为一个行向量，
    #50代表要分的元素的个数
    #
    #facecolor,alpha都是代表颜色的)
    plt.hist(data2,80,normed=True,facecolor='g',alpha = 0.8)
    plt.grid(True)
    plt.show()
