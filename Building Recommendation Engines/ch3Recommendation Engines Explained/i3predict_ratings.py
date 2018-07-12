import os
import csv
from termcolor import colored
import pandas as pd
import i0read_csv

if __name__ == "__main__":
    ratings = pd.read_csv('../data/movie_rating.csv')
    print(ratings)

    pivot_ratings = ratings.pivot_table(columns='critic',
                                        index='title',
                                        values='rating')
    print('pivot_ratings:', type(pivot_ratings))
    print(pivot_ratings.to_string())
    
    sm = pivot_ratings.corr()
    print(sm.to_string())

    print(colored('预测打分=======>', 'red', attrs=['reverse', 'blink']))
    missing_films = list(pivot_ratings[pivot_ratings['Toby'].isnull()].index)
    print(missing_films)

