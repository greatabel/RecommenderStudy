import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.sparse import csr_matrix
from knn_recommender import Recommender

# Read userid-songid-listen_count
song_info = pd.read_csv("data/10000.txt", sep="\t", header=None)
song_info.columns = ["user_id", "song_id", "listen_count"]

# Read song  metadata
song_actual = pd.read_csv("data/song_data.csv")
song_actual.drop_duplicates(["song_id"], inplace=True)

# Merge the two dataframes above to create input dataframe for recommender systems
songs = pd.merge(song_info, song_actual, on="song_id", how="left")
print("count=", len(songs))

songs.to_csv("data/songs.csv", index=False)
df_songs = pd.read_csv("data/songs.csv")
print(df_songs.head())

# count how many rows we have by song, we show only the ten more popular songs
ten_pop_songs = (
    df_songs.groupby("title")["listen_count"]
    .count()
    .reset_index()
    .sort_values(["listen_count", "title"], ascending=[0, 1])
)
ten_pop_songs["percentage"] = round(
    ten_pop_songs["listen_count"].div(ten_pop_songs["listen_count"].sum()) * 100, 2
)

ten_pop_songs = ten_pop_songs[:10]
print("ten_pop_songs=")
print(ten_pop_songs)

song_user = df_songs.groupby("user_id")["song_id"].count()
# Get users which have listen to at least 16 songs
song_ten_id = song_user[song_user > 16].index.to_list()
# Filtered the dataset to keep only those users with more than 16 listened
df_song_id_more_ten = df_songs[df_songs["user_id"].isin(song_ten_id)].reset_index(
    drop=True
)
# convert the dataframe into a pivot table
df_songs_features = df_song_id_more_ten.pivot(
    index="song_id", columns="user_id", values="listen_count"
).fillna(0)

# obtain a sparse matrix
mat_songs_features = csr_matrix(df_songs_features.values)

df_unique_songs = df_songs.drop_duplicates(subset=["song_id"]).reset_index(drop=True)[
    ["song_id", "title"]
]
decode_id_song = {
    song: i
    for i, song in enumerate(
        list(df_unique_songs.set_index("song_id").loc[df_songs_features.index].title)
    )
}

collab_filter_model = Recommender(
    metric="cosine",
    algorithm="brute",
    k=20,
    data=mat_songs_features,
    decode_id_song=decode_id_song,
)
song = "I believe in miracles"
new_recommendations = collab_filter_model.make_recommendation(new_song=song, n_recommendations=10)
print(f"The recommendations for {song} are:")
print(f"{new_recommendations}")
"""
['Nine Million Bicycles', 'If You Were A Sailboat', 'Shy Boy', 'I Cried For You', "Spider's Web", 'Piece By Piece', 'On The Road Again', 'Blues In The Night', 'Blue Shoes', 'Thank You Stars']
"""
