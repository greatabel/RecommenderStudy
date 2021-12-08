import numpy as np
import pandas as pd
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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


songs = pd.read_csv("data/songdata.csv")
print(songs.head())

print(len(songs), " is the count")


songs = songs.sample(n=5000).drop("link", axis=1).reset_index(drop=True)
tfidf = TfidfVectorizer(analyzer="word", stop_words="english")

lyrics_matrix = tfidf.fit_transform(songs["text"])
cosine_similarities = cosine_similarity(lyrics_matrix)
similarities = {}


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

recommendation = {"song": songs["song"].iloc[10], "number_songs": 10}

recommedations.recommend(recommendation)
print(recommendation)
"""
['Sick', 'Eat It', "I Cain't Say No", 'Poppies', 'Older Gods', 'Most Of Us', "I Don't Wanna Work", 'Sifting', 'The Tin Man', "I Don't Know Why"]
"""
