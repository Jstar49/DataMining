import pandas as pd

def ImportData(file):
    '''导入数据文件'''
    data1 = pd.read_excel(file)
    data = data1.iloc[:,:].values.tolist() # 读取特征向量
    b = data1.iloc[0:0, :]
    labels = b.columns.values.tolist()  # 读取特征列表
    return labels, data

def Ex_p(data):
    '''
    计算先验概率
    :param data:
    :return: 返回先验概率 及 先验字典
    '''
    exp = {}
    for pk in data:
        if pk[len(pk)-1] not in exp:
            exp[pk[len(pk)-1]] = 0
        exp[pk[len(pk)-1]] += 1
    exp2 = {}
    for pk in exp:
        exp2[pk] = round(exp[pk] / len(data),3)
    return exp, exp2

def Ex_p_Tiao(exp1, data, label, ind):
    '''
    计算条件概率
    :param exp1: 先验概率
    :param data: 源数据
    :param label: 标签
    :param ind: 位置
    :return:
    '''
    dp = {}
    for pk in exp1:
        kp = 0
        for temp in data:
            if pk == temp[len(temp)-1]:
                if label == temp[ind]:
                    kp += 1
        dp[pk] = round(kp / exp1[pk], 3)
    return dp

def Tian(exp1, labels, data, X):
    '''计算条件概率并返回字典'''
    P = {}
    for label in X:
        # print(label)
        P[label] = Ex_p_Tiao(exp1, data, X[label], labels.index(label))
    return P

def clac_rate(di, exp2):
    '''计算概率'''
    pre = {}
    for r in exp2:
        rat = exp2[r]
        for pk in di:
            rat *= di[pk][r]
        pre[r] = round(rat, 3)
    return pre

def Bayes(labels, data, X):
    '''
    贝叶斯算法计算各概率
    :param labels: 标签
    :param data: 源数据
    :param X: 预测数据
    :return: 预测结果
    '''
    # 计算先验概率
    exp1, exp2 = Ex_p(data)
    print("先验概率：")
    print(exp2)

    P = Tian(exp1, labels, data, X)
    print("条件概率：")
    print(P)
    pre = clac_rate(P, exp2)
    print("预测概率：")
    print(pre)
    return max(pre)

if __name__ == '__main__':
    file_Name = 'data.xlsx'
    labels, data = ImportData(file_Name)
    # 要预测的数据
    X = {'age':'<=30', 'income':'Medium', 'student':'Yes', 'credit_rating':'Fair'}
    print("预测数据为：")
    print(X)
    bay = Bayes(labels,data, X)
    print("预测结果为：")
    print(bay)