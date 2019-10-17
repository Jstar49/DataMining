import numpy as np
import matplotlib.pyplot as plt
import random

def ImportData(filename):
    '''导入数据'''
    data = []
    labels = []
    fil = open(filename)
    for lines in fil.readlines():
        # print(lines)
        lineData = lines.strip().split(',')
        # print(lineData)
        data.append([float(lineData[0]),float(lineData[1])])
        labels.append(float(lineData[2]))
    # print(data)
    # print(labels)
    return data, labels

def SMO(data,labels,C,toler,loopNum):
    '''
    :param data: 数据集
    :param labels: 标签
    :param C: 松弛变量
    :param toler: 误差值
    :param loopNum: 最大循环次数
    :return:
        alphas: 拉格朗日乘子
        b: 函数常量
    '''
    data = np.mat(data)
    # print(data)
    # 矩阵转置，类似于 .T
    labels = np.mat(labels).transpose()
    # print(labels)
    m, n = np.shape(data)
    # print(m,n)

    # 初始化 b 和拉格朗日乘子 alphas
    b = 0
    alphas = np.mat(np.zeros((m, 1)))
    # print(alphas)

    # 当 alphas 改变没有改变时遍历数据的次数
    temp = 0

    while (temp < loopNum):
        # w = calcWs(alphas,data,labels)

        alphasChanges = 0
        for i in range(m):
            # 我们预测的类别 y = w^Tx[i]+b; 其中因为 w = Σ(1~n) a[n]*lable[n]*x[n]
            fxi = float(np.multiply(alphas, labels).T * (data * data[i,:].T)) + b
            # print(fxi)
            # 预测结果与真实结果对比，计算误差Ei
            Ei = fxi - float(labels[i])
            # print(Ei)
            '''
            检测样本(xi,yi)是否满足KKT条件:
            yi*f(i) >= 1 and alpha = 0 (outside the boundary)
            yi*f(i) == 1 and 0 < alpha < C (on the boundary)
            yi*f(i) <= 1 and alpha = C (between the boundary)
            '''
            if ((labels[i]*Ei < -toler) and (alphas[i] < C)) or ((labels[i]*Ei > toler) and (alphas[i] > 0)):
                # 如果满足优化条件，就随机选取一个非i 的一个点，进行优化比较
                j = selectJ(i, m)
                fxj = float(np.multiply(alphas,labels).T * (data*data[j,:].T)) + b
                Ej = fxj - float(labels[j])

                # 选择变量, alpha_i_old,alpha_j_old
                alpha_i_old = alphas[i].copy()
                alpha_j_old = alphas[j].copy()

                #将alpha[j]调整到0~C之间，如果L == H，则continue
                if labels[i] != labels[j]:
                    L = max(0, alpha_j_old-alpha_i_old)
                    H = min(C, C+alpha_j_old-alpha_i_old)
                elif labels[i] == labels[j]:
                    L = max(0, alpha_j_old+alpha_i_old-C)
                    H = min(C,alpha_j_old+alpha_i_old)
                if L == H:
                    print('L == H')
                    continue

                # 计算alpha[j]_new_unc
                eta = -data[i,:]*data[i,:].T - data[j,:]*data[j,:].T + 2*data[i,:]*data[j,:].T
                if eta>=0:
                    continue

                alpha_j_new_unc = alphas[j] - labels[j]*(Ei-Ej)/eta

                # 裁剪alpha[j]:
                if alpha_j_new_unc > H:
                    alphas[j] = H
                elif alpha_j_new_unc < L:
                    alphas[j] = L
                else:
                    alphas[j] = alpha_j_new_unc

                # 更新alpha[i]
                alphas[i] = alpha_i_old + labels[i]*labels[j]*(alpha_j_old - alphas[j])

                # 更新b
                b1 = -Ei - labels[i]*(alphas[i] - alpha_i_old)*data[i,:]*data[i,:].T - labels[j]*(alphas[j] - alpha_j_old)*data[i,:]*data[j,:].T + b
                b2 = -Ej - labels[i]*(alphas[i] - alpha_i_old)*data[i,:]*data[j,:].T - labels[j]*(alphas[j] - alpha_j_old)*data[j,:]*data[j,:].T + b

                if (0 < alphas[i]) and (alphas[i] < C):
                    b = b1
                elif (0 < alphas[j]) and (alphas[j] < C):
                    b = b2
                else:
                    b = (b1+b2)/2.0

                alphasChanges =+ 1
                print('temp: %d :alpha[%d] changed: %d ' % (temp, i,alphasChanges))
        if alphasChanges == 0:
            temp += 1
        else:
            temp = 0
        print('temp number : %d ' % temp)
    return b, alphas



def selectJ(i,m):
    j = i
    while j == i:
        j = int(random.uniform(0, m))
    return j

def calcWs(alphas, dataArr, classLabels):
    """
    基于alpha计算w值
    """
    X = np.mat(dataArr)
    labelMat = np.mat(classLabels).transpose()
    m, n = np.shape(X)
    w = np.zeros((n, 1))
    for i in range(m):
        w += np.multiply(alphas[i] * labelMat[i], X[i, :].T)
    return w

def PlotSVM(data, labels,b,alphas,w):
    plt.xlabel(u'x1')
    plt.ylabel(u'x2')
    plt.xlim(0, 100)
    for i in range(len(labels)):
        # print(data[i])
        if labels[i] == 1:
            plt.scatter(data[i][0], data[i][1],color='blue')
        else:
            plt.scatter(data[i][0], data[i][1], color='green')

    x = np.mat([[0], [100]])
    # x = list([float(10), float(90)])
    y = (-b-w[0, 0]*x)/w[1, 0]

    plt.plot(x, y)

    # 把支持向量标红
    for i in range(len(alphas)):
        if alphas[i] > 0.0:
            plt.scatter(data[i][0], data[i][1],color = 'red')

    plt.show()


if __name__ == '__main__':
    # 导入文件
    filename = 'data.txt'
    data, labels = ImportData(filename)
    # 松弛变量
    C = 0.06
    # 误差值
    toler = 0.001
    # 最大循环数
    loopNum = 40


    b, alphas = SMO(data,labels,C,toler,loopNum)

    # print(alphas)
    # print(b)

    w = calcWs(alphas,data,labels)
    print(w)
    PlotSVM(data,labels,b,alphas,w)