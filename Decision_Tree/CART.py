from math import log
import operator
import numpy as np
import pandas as pd
# from pandas import DataFrame,Series
import plotTree

def ImportData(file):
    data1 = pd.read_excel(file)
    data = data1.iloc[:, :].values.tolist()
    b = data1.iloc[:, :]
    label = b.columns.values.tolist()
    # print(data)
    # print(label)
    return data, label

class MyList(list):
    '''
    用于给 list 添加 hash属性，使之能作为 dict 的 key 值
    '''
    """比普通的list多一个__hash__方法"""
    def __hash__(self):
        # 不能返回hash(self)
        # hash(self)会调用self的本方法，再调用回去，那就没完了(RecursionError)
        # 用的时候要注意实例中至少有一个元素，不然0怎么取(IndexError)
        return hash(self[0])

def ClacGini(labels, data, dot):
    '''计算基尼指数'''
    gini_min = 1
    for pk in range(len(labels)):
        d1 = [0, 0]
        d2 = [0, 0]
        print(labels[pk])
        for i in data:
            if i[dot] == labels[pk]:
                d1[0] += 1
                if i[-1] == '是':
                    d2[0] += 1
            else:
                d1[1] += 1
                if i[-1] == '是':
                    d2[1] += 1
        gini = round(d1[0]/len(data) * (2*d2[0]/d1[0]*(1-d2[0]/d1[0])) + d1[1]/len(data)*(2*d2[1]/d1[1]*(1-d2[1]/d1[1])), 2)
        if gini_min > gini:
            gini_min = gini
    return gini_min


def CART(data, labels):
    # 收集每个label的所有值
    label_con = []
    for i in labels:
        pk = labels.index(i)
        label_num = []
        for k in data:
            label_num.append(k[pk])
        label_con.append([i,list(set(label_num))])
    print(label_con)

    gini_min = 1
    gini_label = labels[0]
    for i in range(len(label_con)):
        if i != len(label_con)-1:
            gini = ClacGini(label_con[i][1], data, i)
            if gini_min > gini:
                gini_min = gini
                gini_label = label_con[i][0]
    return labels.index(gini_label)

def tags(data, i, value):
    '''
    按照某个特征value分类后的数据
    :param data: 数据
    :param i: 当前特征
    :param value: 特征
    :return:
    '''
    tags = []
    for feat in data:
        if feat[i] == value:
            t = feat[:i]
            t.extend(feat[i+1:])
            tags.append(t)
    print("按照特征 "+str(value)+" 分类后的数据："+str(tags))
    return tags

def get_max(list):
    '''
    按照分类后类别数量排序，返回数量较大的
    :param list: 列表
    :return:
    '''
    count = {}
    for i in list:
        if i not in count.keys():
            count[i] = 0
        count[i] += 1
    class_count = sorted(count.items(), key=operator.itemgetter(1), reverse=True)
    print(class_count)
    return class_count[0][0]

def createTree(data, labels):
    '''
    建立决策树
    :param data: 特征数据
    :param labels: 特征
    :return: 决策树
    '''
    classlist = [row[-1] for row in data] # 取特征矩阵最后一列进行分类
    # print(classlist)
    if classlist.count(classlist[0]) == len(classlist):
        return classlist[0]
    if len(data[0]) == 1: # 当data矩阵还剩最后一列时
        return get_max(classlist)
    # best_feat = Feat(data) # 计算信息增益选择最优特征
    best_feat = CART(data, labels)
    best_label = labels[best_feat]
    print("当前最优特征节点："+ str(best_label))
    myTree = {best_label:{}}
    del (labels[best_feat]) # 将选择的特征删除
    feat_values = [row[best_feat] for row in data] # 当前最优特征的特征值
    # print(feat_values)
    vals = set(feat_values)
    for value in vals:
        t_labels = labels[:]
        myTree[best_label][value] = createTree(tags(data, best_feat, value), t_labels)
    # print(myTree)
    return myTree

if __name__ == '__main__':
    datafile = u'data.xlsx' # 数据文件
    data, labels = ImportData(datafile)
    # print(data)
    myTree = createTree(data, labels)
    print("得到的树集合为：")
    print(myTree)
    print("树状图如下图所示！")
    plotTree.createPlot(myTree)

