import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from termcolor import colored


books = pd.read_csv('BX-CSV/BX-Books.csv', sep=';', error_bad_lines=False, encoding="latin-1")
books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication',
                 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']
users = pd.read_csv('BX-CSV/BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
users.columns = ['userID', 'Location', 'Age']
ratings = pd.read_csv('BX-CSV/BX-Book-Ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")
ratings.columns = ['userID', 'ISBN', 'bookRating']

print('-----------------------------------------')
average_rating = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].mean())
average_rating['ratingCount'] = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
h = average_rating.sort_values('ratingCount', ascending=False).head()
print(h)
print('得到最多评价的书籍 并不是平均分最高的')
print(colored('排除没有投过200票的用户 书籍少于100个投票的也排除掉', 
              'red', attrs=['reverse', 'blink']))

counts1 = ratings['userID'].value_counts()
ratings = ratings[ratings['userID'].isin(counts1[counts1 >= 200].index)]
counts = ratings['bookRating'].value_counts()
ratings = ratings[ratings['bookRating'].isin(counts[counts >= 100].index)]
# print(ratings.head(5))
print('把表转化为 2纬矩阵')
ratings_pivot = ratings.pivot(index='userID', columns='ISBN').bookRating
print(ratings_pivot.head(), ratings_pivot.shape)

print('我们找出isbn=0316666343的 打分数第二多的 The Lovely Bones: A Novel')
bones_ratings = ratings_pivot['0316666343']
similar_to_bones = ratings_pivot.corrwith(bones_ratings)
corr_bones = pd.DataFrame(similar_to_bones, columns=['pearsonR'])
corr_bones.dropna(inplace=True)
corr_summary = corr_bones.join(average_rating['ratingCount'])
summary_head = corr_summary[corr_summary['ratingCount']>=300].sort_values('pearsonR', ascending=False).head(10)
print(summary_head)
