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


################ 以下为非必须的，因为训练需要GPU(CUDA)，初期我们可以免费训练一批次 ################
5.

下载神经网络超参数：http://www.vlfeat.org/matconvnet/models/beta16/imagenet-vgg-verydeep-19.mat
然后放在i1picture_style_learning_machine目录下

6.
并在项目根目录下键入：
`python neural_style.py --content 原始图片文件名 --styles 风格图片文件名 --out 生成图片文件名`

例子：
python3 neural_style.py --content s.jpg --styles abel.jpg --out out1.jpg

7.
原理介绍：
这是一个迭代了1000次的例子(使用默认参数),使用 1000-5000 迭代次数就可以有一个很不错的结果，
通过修改其他参数我们可以得到不同的效果

