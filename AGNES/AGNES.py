import pandas as pd

def ImportData(filename):
    '''载入源数据'''
    data1 = pd.read_excel(filename)
    data = data1.iloc[:, :].values.tolist()
    print('源数据库为：')
    print(data)
    return data

def len_p(p,k):
    # print(p,k)
    '''
    计算两点间的距离
    '''
    le = (p[1] - k[1])**2 + (p[2] - k[2])**2
    return le


def Cu_len(k_set, p_set,data):
    '''计算两个簇的最小距离'''
    min_len = len_p(data[k_set[0]-1], data[p_set[0]-1])
    for k in k_set:
        for p in p_set:
            k_p = len_p(data[k-1], data[p-1])
            if min_len >= k_p:
                min_len = k_p
    return min_len

def Set_cu(cu_set,data):
    '''寻找两个最近的簇，并合并'''
    cuu = cu_set[:]
    min_len = Cu_len(cu_set[0],cu_set[1],data)
    cu_list = [cu_set[0],cu_set[1]]
    for kset in cu_set:
        for pset in cu_set:
            if kset != pset:
                kp = Cu_len(kset, pset, data)
                if min_len >= kp:
                    min_len = kp
                    cu_list = [kset,pset]
    for i in cu_list:
        cuu.remove(i)
    temp = []
    for i in cu_list:
        for j in i:
            temp.append(j)
    cuu.append(temp)
    return cuu


def Agnes(data, K):
    sets = []
    for j in data:
        sets.append([j[0]])
    while len(sets) > K:
        sets = Set_cu(sets,data)

    print('\n分类后的簇：')
    print(sets)


if __name__ == '__main__':
    # 载入源数据
    filename = 'data.xlsx'
    data = ImportData(filename)
    # 终止条件规定簇数目
    K = 2
    Agnes(data,K)