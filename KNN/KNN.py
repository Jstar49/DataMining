import numpy as np
import random
import matplotlib.pyplot as plt


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


def getdata():
    # 随机产生数据集
    poa = [[] for i in range(3)]
    for i in poa:
        for k in range(15):
            i.append([random.randint(0, 15), random.randint(0, 15)])
    return poa


def Plot_data(data, point):
    '''绘制 数据集 以及 要分类的随机点'''
    col = ['red', 'blue', 'yellow']  # 类别分色
    for i in range(len(data)):
        for k in data[i]:
            plt.scatter(k[0], k[1], color=col[i], marker='s')
    plt.scatter(point[0], point[1], color='green', marker='o')
    plt.title("The green one is a random point")
    plt.text(18, 15, r'Red: Label A', color="red")
    plt.text(18, 14, r'Blue: Label B', color="blue")
    plt.text(18, 13, r'Yellow: Label C', color="yellow")


def pplen(p1, p2):
    '''计算两点间距离'''
    p11 = np.array(p1)
    p22 = np.array(p2)
    return sum((p11 - p22) * (p11 - p22))


def Compute_len(data, point):
    plen = {}
    for i in data:
        for p in i:
            plen[MyList(p)] = pplen(point, p)
    return plen


def Get_labels(plen, data):
    '''以最近的20个样本作为判断'''
    p = {}
    for k in range(len(data)):
        p[k] = 0
    for i in range(20):
        for k in range(len(data)):
            if plen[i][0] in data[k]:
                p[k] += 1
    return p, plen[19][1]


def KNN(data, point):
    # 计算各点到随机点的距离
    plen = Compute_len(data, point)
    # 给距离排序
    plen = sorted(plen.items(), key=lambda x: x[1], reverse=False)
    # 计算分类及外围距离
    labels, cirl = Get_labels(plen, data)
    label = max(labels.values())
    for i in labels:
        if labels[i] == label:
            label = i
    la = ['A', 'B', 'C']
    label = la[label]  # 预测分类
    return label, cirl ** 0.5


if __name__ == '__main__':
    data = getdata()

    ran_point = [random.randint(0, 15), random.randint(0, 15)]
    print("随机点坐标为：" + str(ran_point))
    Plot_data(data, ran_point)

    label, cirl = KNN(data, ran_point)

    theta = np.arange(0, 2 * np.pi, 0.01)
    x = ran_point[0] + cirl * np.cos(theta)
    y = ran_point[1] + cirl * np.sin(theta)
    plt.plot(x, y)
    plt.show()
    print("预测分类为： " + str(label))