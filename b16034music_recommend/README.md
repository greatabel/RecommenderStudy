## 部署方案

检测部分推荐部署ubuntu或者其他linux，或者osx等类unix系统
其他系统没有经过充分测试

1.
安装python3.6 以上版本

2. 
安装pip3 

3.
（可选，非必须）（创建python3虚拟目录，隔绝不同版本库之间相互影响）
https://docs.python.org/zh-cn/3/tutorial/venv.html


4.
terminal底下进入工程目录(i1picture_style_learning_machine)下，
在requirements.txt同级目录下运行：
pip3 install --upgrade -r requirements.txt


5.
python3 i2evalute.py 
可以查看最终结果

6.
可选项：
python3 i0content_based_recommend.py
运行内容推荐算法
python3 i1collaborative_filters.py
运行协同推荐算法