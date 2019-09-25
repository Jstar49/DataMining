
## KNN(K-近邻)


代码查看：[KNN.py](KNN.py) <br> 
<br>
源数据： 随机产生<br>

 
1)随机产生数据集，并生成要预测类别的点 <br>
2)计算数据集中每个点到预测点的距离 <br>
3)取K个离预测点最近的数据（坐标），在本例中k=20 <br>
4)在K个样本中选出样本类别最多的类别（Label) <br>
5)预测预测点属于Label <br>

注意：K值取值时，不宜过大或过小，否则会出现误差较大的结果 <br>
 

运行结果：<br>
![result](imgs/result.png)<br>

![result1](imgs/result2.png)<br>