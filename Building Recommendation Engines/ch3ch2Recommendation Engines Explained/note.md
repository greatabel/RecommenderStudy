# 推荐引擎的演化

1st是: collaborative filtering （协同过滤）或者neighborhood method recommenders.
       它们有冷启动问题，难以处理数据稀疏情况。

1. 为啦处理大量用户数据稀疏，使用啦Matrix Factorization（矩阵分解）和
  singular value decomposition（奇异值分解）
2. 为啦处理冷启动，“content-based recommendation systems（基于内容的推荐）
   开始发展。这为personalized recommenders systems打开啦大门。
3. 基于内容的推荐虽然解决啦协同过滤的短板，但是也有自己的短板：它们不能
   解决推荐用户偏好之外的新项目，而协同过滤可以。于是混合推荐模型被开发。
4. 随着 基于内容推荐发展，人类扩展啦内容：像地点，时间，群组之类被加入内容。
   随着内存分析工具的进步（像spark），推荐变得实时，大规模可行。
5. 另外一个当前方面是：推荐的着力点开始从机器学习移到神经网络
