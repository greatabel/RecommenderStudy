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


print(colored('Calculating damped mean using k = 5', 'green', attrs=['reverse', 'blink']))
print("ratings['rating'].mean()=", ratings["rating"].mean())
ratings_sum['sum_rating_factor']=ratings_sum['sum_rating'] + 5*(ratings["rating"].mean())
print(ratings_sum.head(10))
ratings_count = ratings.groupby(['movieId'])[['rating']].count()\
                       .rename(columns = {'rating': 'count_rating'}).reset_index()
ratings_count['count_rating_factor'] = ratings_count['count_rating'] + 5
print(ratings_count.head(10))

ratings_damped = pd.merge(ratings_sum,ratings_count[['movieId',
            'count_rating','count_rating_factor']],on=['movieId'],how='left')

print(colored('ratings_damped', 'green', attrs=['reverse', 'blink']))
print(ratings_damped.head(10))
ratings_damped['damped_mean'] = ratings_damped['sum_rating_factor']/ ratings_damped['count_rating_factor']

ratings_mean_dampmean = pd.merge(rating_mean[['movieId','mean_rating']],
    ratings_damped[['movieId','damped_mean']],on=['movieId'],how='left')
ratings_mean_dampmean = ratings_mean_dampmean.sort_values(['mean_rating'], ascending=False)
print(ratings_mean_dampmean.head(10))