import  pandas as pd
import  numpy as np
import math


from termcolor import colored
# https://medium.com/@tomar.ankur287/non-personalised-recommender-system-in-python-42921cd6f971

ratings = pd.read_csv("movies_ratings_tags_csv/ratings.csv",encoding="ISO-8859-1")
movies = pd.read_csv("movies_ratings_tags_csv/movies.csv",encoding="ISO-8859-1")
tags = pd.read_csv("movies_ratings_tags_csv/tags.csv",encoding="ISO-8859-1")

a = ratings[ratings['userId']==320]
print(a.head(5), '\n', a[a['movieId']==260])

TF= tags.groupby(['movieId','tag'], as_index = False, sort = False).count()\
        .rename(columns = {'userId': 'tag_count_TF'})[['movieId','tag','tag_count_TF']]
print('\n', TF.head(5))

tag_distinct = tags[['tag', 'movieId']].drop_duplicates()
# print('\n', tag_distinct.head(5))
DF = tag_distinct.groupby(['tag'], as_index = False, sort= False).count()\
        .rename(columns = {'movieId': 'tag_count_DF'})[['tag', 'tag_count_DF']]
print('\n', DF.head(5))

a = math.log10(len(np.unique(tags['movieId'])))
print('\na=', a)
DF['IDF'] = a - np.log10(DF['tag_count_DF'])
TF = pd.merge(TF, DF, on = 'tag', how = 'left', sort = False)
TF['TF-IDF'] = TF['tag_count_TF']*TF['IDF']
print(TF.head(5))