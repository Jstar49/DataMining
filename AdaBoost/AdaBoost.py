import numpy as np
import math

def ImportData(filename):
    x = []
    y = []
    fi = open(filename)
    for line in fi:
        lineData = line.strip().split(',')
        x.append(int(lineData[0]))
        y.append(int(lineData[1]))
    return x, y

def Clac_Error_point(yu, x, y, sigma):
    # print(yu)
    temp = [[-1, 1], [1, -1]]
    temp1 = []
    e = [0.0, 0.0]
    ent = 1
    for k in range(len(temp)):
        for i in range(len(x)):
            if x[i] < yu:
                if y[i] != temp[k][0]:
                    e[k] += sigma[i]
            else:
                if y[i] != temp[k][1]:
                    e[k] += sigma[i]
        # print(float(e[k]))
        if ent > e[k]:
            ent = e[k]
            temp1 = temp[k]
        # e[k] = e[k] / len(x)
    # print(round(ent, 3))
    ent = round(ent, 4)
    # print(temp1)
    return ent, temp1

def Find_1(x, y, sigma, yu_list):
    '''找到阈值'''
    ent = 1
    returns = []
    for yu in yu_list:
        ent1, temp = Clac_Error_point(yu, x, y, sigma)
        if ent > ent1:
            returns = []
            ent = ent1
            returns.append(ent1)
            returns.append(temp)
            returns.append(yu)
    # print(returns)
    return returns[0], returns[1], returns[2]

def AdaBoost(x, y):
    sigma = []
    for i in range(len(x)):
        sigma.append(1.0 / len(x))
    print('初始sigma : ', sigma)
    #计算可用的阈值
    yu_list = []
    for i in range(len(x)-1):
        # if y[i] != y[i+1]:
            # 阈值
        yu_list.append((x[i]+x[i+1]) / 2.0)
    # print(yu_list)
    # 基础分类器
    function_G = 1
    # 分类器是否完成
    function_isRight = False
    # 存储分类器数据
    function_data = []
    while function_isRight!=True:
        '''
        temp用于存储阈值分类，temp的值为[1,-1]或[-1,1]
        当 X[i] < yu(阈值) 时，预测分类为temp[0]
        当 X[i] > yu(阈值) 时，预测分类为temp[1]
        '''
        ent, temp, yu = Find_1(x, y, sigma, yu_list)

        print('当前阈值 :', yu)
        # print()
        # 计算系数
        alpha = round(1 / 2 * math.log((1 - ent) / ent), 4)
        print('系数 alpha : alpha = ', alpha)

        function_data.append([alpha, temp, yu])

        # Z_m是规范化因子
        Zm = 0
        for k in range(len(x)):
            if (x[k] < yu):
                g = temp[0]
            else:
                g = temp[1]
            Zm = Zm + sigma[k] * math.exp(-alpha * y[k] * g)
        # 更新训练数据的权值分布
        for k in range(len(sigma)):
            if (x[k] < yu):
                g = temp[0]
            else:
                g = temp[1]
            sigma[k] = round((sigma[k] / Zm) * math.exp(-alpha * y[k] * g), 4)
        print('更新sigma : sigma = ', sigma)

        # 输出当前分类器
        function_d = '当前分类器 ： f(x) = ' + str(function_data[0][0])+'*G_1'+'(x)'
        if len(function_d) > 1:
            for pk in range(1, len(function_data)):
                function_d = function_d + '+' + str(function_data[pk][0])+'*G_'+str(pk+1)+'(x)'
        print(function_d)


        # 验证当前分类器效果
        fun_errors = 0
        for pk in range(len(x)):
            pkx = 0
            for pf in function_data:
                if x[pk] < pf[2]:
                    pkx = pkx + pf[0]*pf[1][0]
                else:
                    pkx = pkx + pf[0] * pf[1][1]
            if ((pkx > 0) and (y[pk]!=1)) or ((pkx < 0) and (y[pk]!=-1)):
                fun_errors += 1
        print('当前分类器的误分类点数：', fun_errors)
        if fun_errors == 0:
            function_isRight = True
        print()


if __name__ == '__main__':
    filename = 'data.txt'
    x, y = ImportData(filename)
    print('数据集：')
    print(x)
    print(str(y)+'\n')
    AdaBoost(x, y)