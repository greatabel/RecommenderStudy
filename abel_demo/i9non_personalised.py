import  pandas as pd
import  numpy as np


from termcolor import colored

ratings = pd.read_csv("movies_ratings_tags_csv/ratings.csv",encoding="ISO-8859-1")
movies = pd.read_csv("movies_ratings_tags_csv/movies.csv",encoding="ISO-8859-1")
tags = pd.read_csv("movies_ratings_tags_csv/tags.csv",encoding="ISO-8859-1")


print(colored('Damped means', 'green', attrs=['reverse', 'blink']))

rating_mean = ratings.groupby(['movieId'])[['rating']].mean()\
                     .rename(columns={'rating': 'mean_rating'}).reset_index()
print(rating_mean.head(10))

ratings_sum = ratings.groupby(['movieId'])[['rating']].sum()\
                     .rename(columns={'rating': 'sum_rating'}).reset_index()

print(ratings_sum.head(10))