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
jupyter notebook i2gps_algroithm_spark.ipynb



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






# ------ 总需求 ------

那你的推荐算法会变成2部分：实时推荐根据上面说的权重去2个地方拿推荐结果，然后合并
里面 (hadoop+spark训练部分 是离线提前把我说的距离部分提前算好），给出了结果的中坚结果，缓存起来，
可能是pyspark保存到一个pickle中；然后协同推荐的部分 应该是在 web系统中根据用户的历史流量和喜好数据离线训练出来，然后协同推荐算法会是实时的

你本地也许可以不用维护一套hadoop cluster /spark环境（维护也可以，你不是有虚拟机），到时候第一部分我会在jupyter+pyspark保存训练过程和缓存结果，打包所有的pyspark+hadoop相关的读取/写入代码；第二部分web系统会提供给你，根据我们提供的自动化工具部署起来

还有一点可能要说下：就是怕微博数据可能怕不到需要使用大数据的程度（现在新浪反爬很厉害，估计几百条就启动反爬系统了），
估计还是会需要爬取之外找一些旅游照片数据集，数量才足够

# ------ 附加 ------






