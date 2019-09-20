
## 决策树
*** 
### ID3算法
代码查看：[ID3](ID3.py) <br>
示例： <br>
根据一个人的外貌特征判断性别，特征属性有头发长短、体重、身材 <br>
[数据集](gua.xlsx)： <br><br>
![DataSet](imgs/DataSet.png) <br> 

信息熵计算： <br> 
![ent](imgs/ent.png) 

条件熵计算：<br>
![tiao](imgs/tiao.png)  
 
信息增益计算：<br> 
![gain](imgs/gain.png) 
 
代码运行结果：<br> 
![ID3](imgs/ID3.png) 
 
决策树绘制代码为：[plotTree.py](plotTree.py) 

### C4.5算法
代码查看：[C4.5](C45.py) <br><br>
信息增益率计算：<br> 
![c45](imgs/gain1.png) 

其中IV(a)的计算方式：<br> 
![IV](imgs/IV.png) 

代码运行结果：<br> 
![C45](imgs/C45.png) 

