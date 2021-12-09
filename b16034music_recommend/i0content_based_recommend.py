import numpy as np
import pandas as pd
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

'''
你看第一个机遇内容的推荐，
我们使用的song_data.csv  ，基本5.7w条数据。
我们基本是机遇用户以前听过什么，然后根据内容相似程度，推荐差不多的歌，让用户继续听。这个和其他的用户行为旧没有关系。
比如以前听过范特西，我们可以推荐双节棍啊。准确的说是机遇内容的相似程度。
内容的相似程度怎么衡量呢，我们是把内容根据term frequency–inverse document frequency拆分成词语和评论，
具体可以参考（https://zhuanlan.zhihu.com/p/31197209）
然后我们根据这些的相似程度，做内容相似比较，大的等词语和频率变成归一化数组后，我们对于我们的歌推荐系统，
我们将使用余弦相似性或者其他的明氏距离算相似度，找到最高的，作为内容推荐的依据。
'''

class ContentBasedMusicRecommender:
    def __init__(self, matrix):
        self.matrix_similar = matrix

    def _print_message(self, song, recom_song):
        rec_items = len(recom_song)
        mysongs = []
        print(f"The {rec_items} recommended songs for {song} are:")
        for i in range(rec_items):
            print(f"Number {i+1}:")
            print(
                f"{recom_song[i][1]} by {recom_song[i][2]} with {round(recom_song[i][0], 3)} similarity score"
            )
            mysongs.append(recom_song[i][1])
            print("--------------------")

        print(mysongs)

    def recommend(self, recommendation):
        # Get song to find recommendations for
        song = recommendation["song"]
        # Get number of songs to recommend
        number_songs = recommendation["number_songs"]
        # Get the number of songs most similars from matrix similarities
        recom_song = self.matrix_similar[song][:number_songs]
        # print each item
        self._print_message(song=song, recom_song=recom_song)

# 读取歌曲数据集
songs = pd.read_csv("data/songdata.csv")
print(songs.head())

print(len(songs), " is the count")


songs = songs.sample(n=5000).drop("link", axis=1).reset_index(drop=True)

# term frequency–inverse document frequency拆分成词语和频率
tfidf = TfidfVectorizer(analyzer="word", stop_words="english")

lyrics_matrix = tfidf.fit_transform(songs["text"])
# 计算词语和频率的余弦距离，根据这个度量他们的相似度
cosine_similarities = cosine_similarity(lyrics_matrix)
similarities = {}

# 根据最近余弦距离获得对应的歌曲索引，然后找到歌曲的作者和内容，准备好预处理
for i in range(len(cosine_similarities)):
    # Now we'll sort each element in cosine_similarities and get the indexes of the songs.
    similar_indices = cosine_similarities[i].argsort()[:-50:-1]
    # After that, we'll store in similarities each name of the 50 most similar songs.
    # Except the first one that is the same song.
    similarities[songs["song"].iloc[i]] = [
        (cosine_similarities[i][x], songs["song"][x], songs["artist"][x])
        for x in similar_indices
    ][1:]

print("-" * 20)
recommedations = ContentBasedMusicRecommender(similarities)
# 找到top10的选项，基于内容的
recommendation = {"song": songs["song"].iloc[10], "number_songs": 10}

recommedations.recommend(recommendation)
print(recommendation)
"""
['Sick', 'Eat It', "I Cain't Say No", 'Poppies', 'Older Gods', 'Most Of Us', "I Don't Wanna Work", 'Sifting', 'The Tin Man', "I Don't Know Why"]
"""
