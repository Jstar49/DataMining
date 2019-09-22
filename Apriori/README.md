
## 强关联规则


代码查看：[Apriori.py](Apriori.py) <br> 
<br>
源数据： [data.xlsx](data.xlsx) <br>
![data](imgs/data.png)<br>

第一步，递归算出频繁项目集以及最大频繁项目集：<br>
> 频繁项目集：[['A'], ['B'], ['C'], ['D'], ['E'], ['A', 'B'], ['A', 'C'], ['A', 'D'], ['B', 'C'], ['B', 'D'], ['B', 'E'], ['C', 'D'], ['C', 'E'], ['A', 'B', 'C'], ['A', 'B', 'D'], ['A', 'C', 'D'], ['B', 'C', 'D'], ['B', 'C', 'E'], ['A', 'B', 'C', 'D']]
> 最大频繁项目集： ['A', 'B', 'C', 'D'] 

原理： <br> 
 
支持度的计算：<br> 
![sup](imgs/support.png)<br>
 
置信度的计算：<br>
![con](imgs/confidence.png)<br>
 
提升度的计算：<br>
![lift](imgs/Lift.png)<br>
 
运行结果：<br>
![result](imgs/result.png)<br>
