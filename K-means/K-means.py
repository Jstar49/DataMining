import numpy as np
import random


def ImportData():
    '''导入数据'''
    data = [[1, 1, 4], [2, 1, 2], [1, 2, 3], [2, 2, 5], [4, 3, 6], [5, 3, 9], [4, 4, 1], [5, 4, 2]]
    return data


def Compute_means(pk, meams):
    '''计算距离'''
    tmp = []
    for i in meams:
        op = 0
        for k in range(len(pk)):
            op += (pk[k] - i[k]) * (pk[k] - i[k])
        tmp.append(op)
    return tmp.index(min(tmp))


def Set_1(ron_len, meams, data):
    '''根据均值给源数据分类，产生新簇'''
    t = [[] for i in range(ron_len)]
    for pk in data:
        t[Compute_means(pk, meams)].append(data.index(pk))
    return t


def Compute_new_means(t, data):
    '''计算新簇的均值'''
    tmp = []
    for pk in t:
        means = 0
        for i in pk:
            means += np.array(data[i])
        means = means / len(pk)
        tmp.append(list(means))
    return tmp


def K_Means(data):
    ron = []
    while len(ron) < len(data[0]):
        num = random.randint(0, len(data) - 1)
        if num not in ron:
            ron.append(num)
    print("随机初始点为：" + str(ron) + "\n")
    # 初始均值
    meams = []
    for i in ron:
        meams.append(data[i])
    go = True
    go_num = 1
    while go:
        t = Set_1(len(ron), meams, data)
        meam = Compute_new_means(t, data)
        if meam == meams:
            go = False
        meams = meam

        print("第 " + str(go_num) + " 次迭代：")
        go_num += 1
        print("新簇：" + str(t))
        print("新均值：" + str(meams))
        print()

    print("最后的簇分类为:")
    print(t)


if __name__ == '__main__':
    data = ImportData()
    K_Means(data)

