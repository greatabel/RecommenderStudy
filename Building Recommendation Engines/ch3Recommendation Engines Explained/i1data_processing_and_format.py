import os
import csv
import pandas as pd
import i0read_csv

if __name__ == "__main__":
    ratings = pd.read_csv('../data/movie_rating.csv')
    print(ratings)
    pivot_ratings = ratings.pivot_table(columns='critic',
                                        index='title',
                                        values='rating')
    print(pivot_ratings)

