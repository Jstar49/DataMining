import matplotlib.pyplot as plt
import pandas as pd

def ImportData(filename):
    '''载入源数据'''
    data1 = pd.read_excel(filename)
    data = data1.iloc[:,:].values.tolist()
    print('源数据库为：')
    print(data)
    return data

def PlotData(data):
    '''绘制源数据'''
    for k in data:
        plt.scatter(k[1], k[2], color='green', marker='o')
        plt.text(k[1], k[2], str(k[0]), color="red")

def len_p(p,k):
    '''
    计算两点间的距离
    '''
    le = ((p[1] - k[1])**2 + (p[2] - k[2])**2)**0.5
    return le

def Set_r(p,data,r):
    '''计算以p为簇中心，r为半径内的所有对象'''
    set_r = []
    for k in data:
        if len_p(p,k) <= r:
            set_r.append(k[0])
    return set_r

def Scan(data,r,MinPts):
    '''
    对数据库中的对象进行迭代，寻找在半径r内，对象密度大于MinPts的对象，并搜索该对象密度可达的对象，
    连接成簇
    :param data: 源数据
    :param r: 对象区域半径
    :param MinPts: 区域最小对象数目
    :return:
    '''
    # 所有簇集合
    cu_set = []
    for k in data:
        set1 = Set_r(k,data,r)
        # print(str(k[0])+str(set1))
        if len(set1) >= MinPts:
            # print(k)
            flags = -1
            # flags
            for pk in range(len(cu_set)):
                # print(pk)
                if k[0] in cu_set[pk]:
                    # print(cu_set)
                    # cu_set[pk] += set1
                    flags = pk
            if flags != -1:
                cu_set[flags] =list(set(cu_set[flags] + set1))
            if flags == -1:
                cu_set.append(set1)
    # print(cu_set)
    return cu_set

if __name__ == '__main__':
    # 导入数据
    filename = 'data.xlsx'
    data = ImportData(filename)
    # 给定半径R
    r = 1
    # 给定MinPts
    MinPts = 4
    # 绘制数据
    PlotData(data)
    cu_set = Scan(data,r,MinPts)
    print('\n共有 '+ str(len(cu_set)) + ' 个簇：')
    for k in cu_set:
        print('簇'+str(cu_set.index(k)+1)+ ': '+ str(k))
    plt.show()