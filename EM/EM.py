import math
import numpy as np

def Clac_mu(y, theta):
    pi = theta[0]
    p = theta[1]
    q = theta[2]
    mu = []
    # E步，计算在模型参数pi,p,q下观测数据y来自投掷硬币B的概率
    for j in y:
        u = (pi*math.pow(p,j)*math.pow(1-p,1-j)) / (pi*math.pow(p,j)*math.pow(1-p,1-j) + (1-pi)*math.pow(q,j)*math.pow(1-q,1-j))
        mu.append(u)
    # M步，计算模型参数的新估计值
    pi_new = sum(mu) / len(y)
    p_new = sum(mu[i]*y[i] for i in range(len(y))) / sum(mu)
    q_new = sum((1-mu[i])*y[i] for i in range(len(y))) / sum((1-mu[i]) for i in range(len(y)))
    return [pi_new, p_new, q_new]


def EM(y, theta, toler):
    loop_is = True
    # 反复迭代
    while loop_is:
        theta_new = Clac_mu(y, theta)

        if np.abs(theta_new[0] - theta[0]) < toler:
            loop_is = False
        else:
            theta = theta_new
        print(theta)
    return theta_new

if __name__ == '__main__':
    y = [1, 1, 0, 1, 0, 0, 1, 0, 1, 1]
    theta = [0.46, 0.55, 0.67]
    # 迭代停止条件
    toler = 0.0004
    theta_new = EM(y,theta, toler)
    print('模型参数theta的极大似然估计是：',theta_new)