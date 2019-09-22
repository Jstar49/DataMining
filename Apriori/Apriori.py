import pandas as pd
import prettytable as pt

# 用来存放所有的频繁项目集
fre_item = []
# 存放最大频繁项目集
max_fre = []

def Road_Data(file):
    '''
    导入数据
    :param file: 文件名
    :return: 处理后的数据
    '''
    data1 = pd.read_excel(file)
    data1 = data1.iloc[:, 1:].values.tolist()
    data = [[] for i in range(len(data1))]
    j = 0
    for i in data1:
        for k in i:
            if pd.isnull(k): # 判断是否为空
                continue
            data[j].append(k)
        j += 1
    return data

def dict_list(d):
    '''
    将Dict 的 keys 组成列表
    :param d: Dict
    :return:
    '''
    l1 = []
    for i in d:
        # print(i)
        l1.append(i)
    return l1

def Sup(data, minsup_count):
    '''
    生成1-频繁项目集
    :param data:
    :param minsup_count:
    :return:
    '''
    sup_count = {}
    # 计算支持数
    for i in data:
        for value in i:
            if value not in sup_count.keys():
                sup_count[value] = 0
            sup_count[value] += 1
    # 去掉 支持数 < minsup_count 的数据
    sup_count1 = {}
    for i in sup_count:
        if sup_count[i] >= minsup_count:
            sup_count1[i] = sup_count[i]

    return sup_count

def to_sup(sup, data, num_sup):
    '''
    将k-频繁项目集重新组合，生成k+1-项目集，用来挑选出k+1-频繁项目集
    :param sup: k-频繁项目集
    :param data:
    :param num_sup: 当前周期
    :return:
    '''
    fre = []
    for i in sup:
            for tmp in sup:
                t = [row for row in i]
                for temp in tmp:
                    if (temp not in i) and (temp not in t) and len(t) <= num_sup:
                        t.append(temp)
                if t not in fre:
                    fre.append(t)
    fre_k = []
    for i in fre:
        if len(i) == num_sup:
            fre_k.append(i)
    return fre_k

def Sup_gen(data, fre, minsup_count):
    '''
    计算出 k-项目集 fre 的支持度，并筛选出 支持度 >= minsup_count 的元素
    :param data: 源数据集
    :param fre: k-项目集
    :param minsup_count: 最小支持度
    :return: k-项目集的支持度
    '''
    pre = {}
    for i in fre:
        i = MyList(i)
        for t in data:
            flag = 0
            for k in i:
                if k in t:
                    flag += 1
                if flag == len(i):
                    if i not in pre.keys():
                        pre[MyList(i)] = 0
                    pre[i] += 1
    pre_1 = {}
    for i in pre:
        if pre[i] >= minsup_count:
            pre_1[i] = pre[i]
    pre_2 = {}
    pre_2_1 = []
    for i in pre_1:
        si = set(i)
        if si not in pre_2_1:
            pre_2[i] = pre_1[i]
            pre_2_1.append(si)
    return pre_2

def gen(data, sup_1, minsup_count):
    '''
    使用函数循环生成频繁项目集
    :param data: 源数据
    :param sup_1: 1-频繁项目集
    :param minsup_count: 最小支持度
    :return:
    '''
    len_time = len(sup_1) # 循环周期
    fre_2 = [i for i in sup_1]
    print(len_time)
    for i in range(2, len_time+1):
        print("生成"+str(i)+"+频繁项目集：")
        print("支持度：")
        temp_sup = to_sup(fre_2, data, i)
        temp_sup1 = Sup_gen(data, temp_sup, minsup_count)
        print(temp_sup1)
        print(str(i)+"-频繁项目集：")
        fre_2 = dict_list(temp_sup1)
        print(fre_2)
        if len(fre_2)>=1:
            del max_fre[:]
        for k in fre_2:
            fre_item.append(k)
            max_fre.append(k)
        print("-" * 40)


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

def in_list(tmp):
    '''
    判断 tmp 是否在 max_fre 列表中
    :param tmp:
    :return:
    '''
    flag = 0
    for pl1 in max_fre:
        for pk in tmp:
            if pk in pl1:
                flag += 1
    if flag >= len(tmp):
        return True
    return False

def Set_rules(data):
    '''
    生成关联规则矩阵
    :return:
    '''
    tmp1 = []
    strong = []
    for pk in fre_item:
        if in_list(pk):
            tmp1.append(pk)
    for pk in max_fre:
        tmp1.remove(pk)
    for pk in tmp1:
        for i in max_fre:
            tmp2 = []
            for k in i:
                if k not in pk:
                    tmp2.append(k)
            strong.append((pk, tmp2, Confidence(pk, tmp2, data)))
    return strong

def Confidence(temp1, temp2, data):
    '''
    计算confidence
    :param temp:
    :param data:
    :return:
    '''

    px = 0
    pxy = 0
    for pk in data:
        if set(temp1) <= set(pk):
            px += 1
    px = float(px / len(data)) # temp[0] 的支持度
    pl = temp1+temp2
    for pk in data:
        if set(pl) <= set(pk):
            pxy += 1
    pxy = float(pxy / len(data))
    return round(pxy / px, 2)

def Rules(data,minconfidence, minsupport):
    '''
    生成强关联规则
    :param data:
    :return:
    '''
    strong_list = Set_rules(data)
    tb = pt.PrettyTable(["规则", 'confidence', 'support', '是否为强关联'])
    for pk in strong_list:
        is_not = 'No'
        if pk[2] > minconfidence:
            is_not = 'Yes'
        tb.add_row([str(pk[0])+"-->"+str(pk[1]), pk[2], minsupport, is_not])
    print(tb)

if __name__ == '__main__':
    data = Road_Data("data.xlsx") # 导入数据
    minsup_count = 2 # 最小支持度
    minsupport = 0.4 #
    minconfidence = 0.6
    print("源数据为:")
    for i in data:
        print(i)
    # 生成1-频繁项目集
    print("-"*40)
    print("生成1-频繁项目集：")
    sup_1_count = Sup(data, minsup_count)
    print("支持度：")
    sup_1_count1 = {}
    for i in sup_1_count:
        sup_1_count1[MyList(list(i))] = sup_1_count[i]
    print(sup_1_count1)
    sup_1 = dict_list(sup_1_count) # 将dict 的 key组成一个列表
    fre_1 = []
    for i in sup_1:
        k = []
        k.append(i)
        fre_1.append(k)
    print("1-频繁项目集：")
    print(fre_1)
    for i in fre_1:
        fre_item.append(i)
    print("当前的频繁项目集：")
    print(fre_item)
    print("-"*40)

    gen(data, fre_1, minsup_count)
    print("所有的频繁项目集：")
    print(fre_item)
    print("最大频繁项目集：")
    print(max_fre)

    print("-"*40)
    print("生成关联规则：")
    Rules(data, minconfidence, minsupport)
