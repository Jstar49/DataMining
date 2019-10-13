## AGNES
 
代码查看：[AGNES.py](AGNES.py) <br>
<br> 
源数据：[data.xlsx](data.xlsx) <br>
 
算法描述：<br> 
输入：包含N个对象的数据库，终止条件簇的数目k <br>
输出：k个簇，达到终止条件规定的簇数目 <br>
<br> 

将每个对象当成一个初始簇 <br>
Repeat: <br>
&emsp;&emsp;根据两个簇中最近的数据点找到最近的簇；<br>
&emsp;&emsp;合并两个簇，生成新的簇的集合；<br>
Until 达到定义的簇的数目 <br>
 
<br> 

结果：<br> 
![result](imgs/result.png)