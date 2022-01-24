from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import fuzz
import numpy as np

"""
KNN是一种instance-based learning，属于lazy learning， 
即它没有明显的前期训练过程，而是程序开始运行时，把数据集加载到内存后，就可以直接开始分类。
其中，每次判断一个未知的样本点时，就在该样本点附近找K个最近的点进行投票，这就是KNN中K的意义，通常K是不大于20的整数

用于协同过滤
"""


class Recommender:
    def __init__(self, metric, algorithm, k, data, decode_id_song):
        self.metric = metric
        self.algorithm = algorithm
        self.k = k
        self.data = data
        self.decode_id_song = decode_id_song
        self.data = data
        self.model = self._recommender().fit(data)

    def make_recommendation(self, new_song, n_recommendations):
        recommended = self._recommend(
            new_song=new_song, n_recommendations=n_recommendations
        )
        print("... Done")
        return recommended

    def _recommender(self):
        return NearestNeighbors(
            metric=self.metric, algorithm=self.algorithm, n_neighbors=self.k, n_jobs=-1
        )

    def _recommend(self, new_song, n_recommendations):
        # Get the id of the recommended songs
        recommendations = []
        recommendation_ids = self._get_recommendations(
            new_song=new_song, n_recommendations=n_recommendations
        )
        # return the name of the song using a mapping dictionary
        recommendations_map = self._map_indeces_to_song_title(recommendation_ids)
        # Translate this recommendations into the ranking of song titles recommended
        for i, (idx, dist) in enumerate(recommendation_ids):
            recommendations.append(recommendations_map[idx])
        return recommendations

    def _get_recommendations(self, new_song, n_recommendations):
        # Get the id of the song according to the text
        # 获取歌曲id
        recom_song_id = self._fuzzy_matching(song=new_song)
        # Start the recommendation process
        print(f"Starting the recommendation process for {new_song} ...")
        # Return the n neighbors for the song id
        # 根据knn的规则找到最近邻居
        distances, indices = self.model.kneighbors(
            self.data[recom_song_id], n_neighbors=n_recommendations + 1
        )
        return sorted(
            list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())),
            key=lambda x: x[1],
        )[:0:-1]

    def _map_indeces_to_song_title(self, recommendation_ids):
        # get reverse mapper
        return {
            song_id: song_title for song_title, song_id in self.decode_id_song.items()
        }

    def _fuzzy_matching(self, song):
        match_tuple = []
        # get match
        for title, idx in self.decode_id_song.items():
            ratio = fuzz.ratio(title.lower(), song.lower())
            if ratio >= 60:
                match_tuple.append((title, idx, ratio))
        # sort
        match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
        if not match_tuple:
            print(f"The recommendation system could not find a match for {song}")
            return
        return match_tuple[0][1]
