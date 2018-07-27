import  pandas as pd
import  numpy as np


from termcolor import colored
# https://medium.com/@tomar.ankur287/non-personalised-recommender-system-in-python-42921cd6f971

ratings = pd.read_csv("movies_ratings_tags_csv/ratings.csv",encoding="ISO-8859-1")
movies = pd.read_csv("movies_ratings_tags_csv/movies.csv",encoding="ISO-8859-1")
tags = pd.read_csv("movies_ratings_tags_csv/tags.csv",encoding="ISO-8859-1")

a = ratings[ratings['userId']==320]
print(a.head(5), '\n', a[a['movieId']==260])