1.
安装python3.6 以上版本

2. 
安装pip3 
（如果网速慢 可以pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package  把some-package替换成自己的慢的包 )

3.
可选  可以不做（创建python3虚拟目录，隔绝不同版本库之间相互影响）
https://docs.python.org/zh-cn/3/tutorial/venv.html

4.
4.1
terminal底下进入工程目录下，在requirements.txt同级目录下运行：
pip install --upgrade -r requirements.txt

5.
模拟运行在:
python3 i1wsgi.py



6.
浏览器访问：

http://localhost:5000/home

已经注册好的管理员账号 可以直接登录：
管理员1
username: greatabel1@126.com
password: abel
你也可以自己注册和登录

管理员2
username: admin@126.com
password: admin

-------------------
一般用户测试账号:(geust_test)
username:test@126.com
password: test

7.
个人主页： http://localhost:5000/profile










# ---- requirement ----




1. 爬虫系统
scrapy+python3 + selenium chromiunm

2.
网站+ 垂直搜索部分
网站前后端，垂直搜索的载体：bootstrap + vue.js + flask + numpy/pandas 


3.
搜索算法估计基于文本搜索 （文本搜不到的久远数据基于Elasticsearch搜索，可选，根据情况实施）
这个搜索只有很老数据是基于es的，近期数据库的数据都是我们自己实现搜索算法（比如文本模糊搜索的相似度算法
我们实现编辑距离的算法，Levenshtein距离和Jaro-Winkler距离等，
甚至有时间还可以做相余弦相似度词袋模型的算法 综合实现）

4.
推荐系统部分
协同过滤算法，基于pandas/numpy实现协同过滤

看沟通记录买家有疑惑对于协同过滤推荐，我解释下：
4.1. 由于我们将来有自己的网站（我们所有爬虫，搜索，推荐构成了一个在线平台），我们那时候就有了用户行为数据：
从网站、移动应用程序或其他渠道中收集用户的行为数据，如用户浏览历史、购买历史。
而且历史行为数据集我们会自己构建出离线数据

4.2
基于协同过滤的推荐：使用协同过滤算法来分析用户行为数据，识别用户之间的相似性，并预测用户的兴趣。
对于具有相似兴趣的用户，推荐他们可能喜欢的产品或内容。

4.3
基于内容推荐的推荐：对于没有足够行为数据的新用户，或者推荐系统无法从用户行为数据中发现明显的模式和相似性的情况，
使用内容推荐算法来推荐内容。这种算法通过分析产品或内容的属性和特征，向用户推荐与他们喜欢的内容相似的其他内容。
这块可能主要利用文本相似度算法（各种相似度算法我们进行一个综合）

4.4
结合协同过滤和内容推荐：结合协同过滤和内容推荐的结果，只是自己预先定义一个比例而已（比如50%协同推荐+50%相似度）

5.
5.1
实现用户系统（注册，登陆，账号信息管理，比如修改密码和用户信息等）
5.2
个人主页功能，个人主页可以增删改查自己的introduction信息，introduction可以包含“兴趣，爱好，性格介绍，自我介绍”
5.3
接入性格等因素到第4部分的推荐系统算法中，作为基于内容推荐的一种因素，推荐权重可以设置


