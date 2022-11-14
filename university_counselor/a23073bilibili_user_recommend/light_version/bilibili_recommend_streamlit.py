import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import re
import jieba
import wordcloud
import matplotlib.pyplot as plt
from IPython.display import HTML
from sklearn.manifold import TSNE#使用t-SNE降维
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.cluster import KMeans
from collections import Counter
from gensim import similarities

def read_json(json_file):
	"""定义一个读取json等方法, 返回title"""
	with open(json_file, 'rt',encoding='utf-8') as f:
		text = f.read()

		# 如果文件是空的，返回none
		if len(text) < 300:
			return None
		else:
			if not text.endswith(']'):
				text = text + ']'
			# 解析内容
			dic_list = eval(text.replace(',,',','))
			return dic_list

def get_all_user_data(folder,files):
	"""定义一个读取整个文件夹用户数据的方法"""
	data = []
	used_files = []
	print("读取用户数据...")
	# 读取每一个文件
	for json_file in files:
		json_file = os.path.join(folder,json_file)
		# 对于小于10kb的文件，忽视
		if os.path.getsize(json_file)/1024 < 10:
			continue
		# 提取用户id
		user_id = json_file.split('_')[-1].rstrip('.json')
		# 读取文件
		dic_list  = read_json(json_file)
		if dic_list==None:
			continue
		else:
			contents = []
			# 提取最新50条
			num = 50
			for content in dic_list[:num if len(dic_list)>num else len(dic_list)]:
				# 提取内容
				title = content.get('item').get('title')
				desc = content.get('item').get('desc')
				if title!=None:
					contents.append(title)
				if desc!=None:
					contents.append(desc)
			# 如果没提取到
			if len(contents) > 0:
				data.append([user_id,' '.join(contents),json_file])
	data = pd.DataFrame(data,columns=['user_id','post','file'])
	return data


def get_stop_words(stop_words_file):
	#读取停用词
	with open(stop_words_file, encoding='utf-8') as file:
		words = file.readlines()
	stop_words = [word.strip().replace('\n', '') for word in words]
	return stop_words

def remove_punctuation(line):
	"""定义删除除字母,数字，汉字以外的所有符号的函数"""
	line = str(line)
	if line.strip()=='':
		return ''
	rule = re.compile(u"[^a-zA-Z0-9\u4E00-\u9FA5]")
	line = rule.sub(' ',line)
	return ' '.join(line.split())

def extract_chinese(txt):
	"""提取中文"""
	s = ''
	pattern = re.compile("[\u4e00-\u9fa5]")
	for i in txt:
		s = s + (' ' if i==' ' else "".join(pattern.findall(i)))
	return ' '.join(s.split())

def segment(text,word_len_limit=1):
	"""定义一个jieba分词器，并去除掉停用词，返回一个空格分开词的字符串"""
	words = jieba.cut(text,cut_all=False)
	words = [w.replace(' ','') for w in words if w.replace(' ','') not in STOPWORDS_zh]
	# 返回连接分词再去除多余空格返回
	return [word for word in ' '.join(words).split() if len(word)>=word_len_limit]

### 画词云图
def plot_wordcloud(texts,title='',font_file = '/System/Library/fonts/PingFang.ttc'):

	w = wordcloud.WordCloud(
	width = 1600,height=1200,background_color='white',
	font_path = font_file
	)
	w.generate(texts)
	# w.to_file('word_cloud.png')
	fig = plt.figure(dpi=150)
	plt.imshow(w,interpolation='catrom')
	plt.axis('off')
	plt.title(title)
	# plt.savefig('词云图.png',dpi=400)
	# plt.show()
	return fig

def text_extract(texts:list,vocabulary=None,model_type = 'tfidf',n_features = 1000):
	"""
	tf or tfidf提取文本特征
	Params
	- texts - 文本列表
	- vacabulary - 预定义的
	"""

	print(f"Extracting {model_type} features...")
	if model_type == 'tfidf':
		Vectorizer = TfidfVectorizer
	elif model_type =='tf':
		Vectorizer = CountVectorizer
	else:
		raise Exception("model_type should be tfidf or tf")
	vectorizer = Vectorizer(
						max_df=0.95,
						min_df=2, # 最低门槛（doc frequency）
						max_features=n_features,# how many words
						vocabulary= vocabulary # vacabs
						)
	array = vectorizer.fit_transform(texts).toarray()
	print(f"arr shape: {array.shape}")
	df_array = pd.DataFrame(array,columns=vectorizer.get_feature_names_out())
	return df_array,vectorizer


# K-means聚类算法进行聚类分析
def which_k_best(X,max_k_limit):
	"""
	使用手肘法确定最佳聚类数目k
	Params
	- X - 要聚类的数据
	- max_k_limit - 最大的k值
	"""

	wcss = []
	#使用手肘法确定聚类数目
	for i in range(1, max_k_limit+1):
		kmeans = KMeans(n_clusters=i, max_iter=300, n_init=10)
		kmeans.fit(X)
		wcss.append(kmeans.inertia_)
	plt.figure(figsize=(8,5))
	plt.plot(range(1, max_k_limit+1), wcss)
	plt.xlim(1,10,1)
	plt.title('SSE Method for Kmeans')
	plt.xlabel('Number of clusters')
	plt.ylabel('SSE')
	plt.savefig('SSE_method_for_kmeans.png',dpi=300)
	plt.show()

# run
# which_k_best(X,10

def train_kmeans(X,n_cluster):
	"""
	kmeans聚类算法
	Params
	- X - 传入的矩阵
	- n_cluster - 聚类数量
	Returns
	- km_model - 训练过的聚类模型
	- clusters - 预测的X的clusters
	"""
	print("kmeans training")

	km_model = KMeans(n_clusters=n_cluster)
	# 训练模型
	km_model.fit(X)
	# 预测cluster
	clusters = km_model.predict(X)
	print("Cluster count:\n",Counter(clusters))
	return km_model,clusters

def visualize_cluster(X,clusters,title='Kmeans'):
	"""
	使用tsne将高维（>=3)的数据降维并可视化成二维散点图的方法
	Params
	- X - 要降维的矩阵
	- clusters - 每一行对应的cluster
	"""
	sns.set()
	ts = TSNE(n_components=2,init='random',learning_rate='auto')
	#进行数据降维,降成2维
	ts.fit_transform(X)
	# 把多维数据压缩成二维数据，方便进行散点图可视化
	tsne = pd.DataFrame(ts.embedding_).rename(columns={0:'x',1:'y'})
	# 二维数据可视化散点图
	plt.figure(figsize=(10,10))
	dd = pd.concat([tsne,pd.Series(clusters).rename("cluster")],axis=1)
	sns.scatterplot(data=dd,x='x',y='y',hue='cluster',palette='Dark2',sizes=600)
	plt.title(title,fontsize=15)
	plt.savefig(title+'clusters.png')
	plt.show()

@st.cache
def running_main_train():
	# 读取数据
	folder = './text_datas/'
	files = [file for file in os.listdir(folder) if file.endswith('.json')]
	files = sorted(files)
	# 读取数据
	data = get_all_user_data(folder,files)
	# 保存userid
	# with open("user_id_list.txt",'w') as f:
	# 	f.write('\n'.join(list(data['user_id'])))
	# print("saved user list")
	# visualize_cluster(X,clusters)
	# trainning model
	# 处理数据
	global STOPWORDS_zh
	stop_words_file = 'cn_stopwords.txt'
	STOPWORDS_zh = get_stop_words(stop_words_file)
	data['post'] = data['post'].map(lambda x: ' '.join(segment(extract_chinese(remove_punctuation(x)))))
	# 使用tfidf将文本转化成矩阵
	X,vectorizer = text_extract(data['post'],n_features=300)
	# 训练kmeans
	km_model,clusters  = train_kmeans(X,10)
	data['clusters'] = clusters
	# 文本相似度算法，推荐相似度高的用户
	# 计算用户间的相似度

	sim_matrix = similarities.SparseMatrixSimilarity(X.values,num_features=X.shape[1])
	# 生成相似度矩阵
	df_sim = pd.DataFrame(sim_matrix,index=data['user_id'],columns=data['user_id'])
	return data,df_sim


def kmeans_recommend(user_id,data,nums = 10):
	"""使用kmeans推荐相似用户"""
	# 找到用户类别
	c = data[data['user_id']==user_id].iloc[0]['clusters']
	# 推荐相同类别
	users = data[data['clusters']==c]['user_id']
	# 返回用户id
	return users.sample(nums if len(users) > nums else len(users)).values.tolist()

def sim_recommend(user_id,df_sim,nums=10):
	"""使用文本相似度算法推荐用户"""
	# 找到相似度高的用户
	users = df_sim[user_id].sort_values(ascending=False)
	# 返回推荐用户
	return list(users.iloc[1:nums+1].index)


############# web界面
# streamlit run **.py
data,df_sim = running_main_train()
data[['user_id']].to_csv("能够使用的user_ids.csv")
st.markdown("## Bilibili用户推荐系统")
user_id = st.text_input("请输入用户id")
start = st.button("开始推荐")
if user_id!= '' and start:
	try:
		sim_users= sim_recommend(user_id,df_sim)
		# sim_users_url = ['https://space.bilibili.com/'+ str(x) + '/dynamic' for x in sim_users]
		sim_users_url = ['<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format('https://space.bilibili.com/'+ str(x) + '/dynamic', x) for x in sim_users]

		kmeans_users = kmeans_recommend(user_id,data)
		# kmeans_users_url = ['https://space.bilibili.com/'+ str(x) + '/dynamic' for x in kmeans_users]
		kmeans_users_url = ['<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format('https://space.bilibili.com/'+ str(x) + '/dynamic', x) for x in kmeans_users]

		fig = plot_wordcloud(' '.join(data[data['user_id']==user_id]['post']))
		col1,col2 = st.columns([1,1])
		with col1:
			st.markdown(f"#### 您输入的用户id")
			st.markdown(f"##### {user_id}")
		with col2:
			st.markdown(f"#### 用户发帖词云")
			st.pyplot(fig)
		col3,col4 = st.columns([1,1])
		with col3:
			st.markdown(f"#### 相似度算法推荐")
			# without clickable url
			# st.table(pd.DataFrame({'用户id':sim_users}))
			# st.table(df)

			# st.table(pd.DataFrame({'用户id':sim_users_url}))
			df=pd.DataFrame({'用户id':sim_users_url})
			df = df.to_html(render_links=True, escape=False)
			st.write(df, unsafe_allow_html=True)
		with col4:
			st.markdown(f"#### Kmeans算法推荐")
			# st.table(pd.DataFrame({'用户id':kmeans_users}))
			# st.table(pd.DataFrame({'用户id':kmeans_users_url}))
			df=pd.DataFrame({'用户id':kmeans_users_url})
			df = df.to_html(render_links=True, escape=False)
			st.write(df, unsafe_allow_html=True)


	except:
		st.error("您输入的用户id不存在！")
