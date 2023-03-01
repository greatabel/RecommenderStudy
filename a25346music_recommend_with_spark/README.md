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

新开一个cmd：
jupyter notebook i2music_spark.ipynb



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



8.






# ------ 总需求 ------

主要部分是音乐的协同过滤推荐和spark做大数据分析和可视化吧，
那我们的web系统还是得有用户系统  还有注册、登陆、个人主页维护，
我们才能根据用户喜好和浏览历史数据在整个用户历史数据上做协同过滤推荐哈


# ------ 附加 ------

