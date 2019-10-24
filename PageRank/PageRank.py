import numpy as np

def ImportData(filename):
    fi = open(filename)
    data = []
    for line in fi:
        lineData = line.strip().split(' ')
        data.append(lineData)
    return data

if __name__ == '__main__':
    filename = 'data.txt'
    data = ImportData(filename)
    nodes = []
    print('节点链接为：')
    for i in data:
        print(i[0],'-->',i[1])
        if i[0] not in nodes:
            nodes.append(i[0])
        if i[1] not in nodes:
            nodes.append(i[1])

    N = len(nodes)
    node_set = {}
    pk = 0
    for i in nodes:
        node_set[i] = pk
        pk += 1
    for i in data:
        i[0] = node_set[i[0]]
        i[1] = node_set[i[1]]

    # 生产S矩阵
    S = np.zeros([N, N])
    for i in data:
        S[i[1], i[0]] = 1

    # 计算比例
    for i in range(N):
        sum_d = sum(S[:, i])
        for j in range(N):
            S[j, i] /= sum_d
    # alpha参数
    alpha = 0.85
    # 计算A矩阵
    A = alpha*S + (1-alpha) / N * np.ones([N, N])
    # print(A)

    p1 = np.ones(N) / N
    p2 = np.zeros(N)

    # 迭代停止误差区间
    toler = 1
    # 开始迭代
    k = 1
    while toler > 0.00001:
        p2 = np.dot(A, p1)
        toler = p2 - p1
        toler = max(map(abs, toler))
        p1 = p2
        print('第 ',k ,' 次迭代结果：', p1)
        k += 1
    print('迭代结束!\n最终的PR值为：',p1)