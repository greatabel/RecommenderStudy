import  pandas as pd
import  numpy as np


from termcolor import colored

ratings = pd.read_csv("movies_ratings_tags_csv/ratings.csv",encoding="ISO-8859-1")
movies = pd.read_csv("movies_ratings_tags_csv/movies.csv",encoding="ISO-8859-1")
tags = pd.read_csv("movies_ratings_tags_csv/tags.csv",encoding="ISO-8859-1")
