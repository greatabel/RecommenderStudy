import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from termcolor import colored

# http://www.ituring.com.cn/article/497300
books = pd.read_csv('BX-CSV/BX-Books.csv', sep=';', error_bad_lines=False, encoding="latin-1")
books.columns = ['ISBN', 'bookTitle', 'bookAuthor', 'yearOfPublication',
                 'publisher', 'imageUrlS', 'imageUrlM', 'imageUrlL']
users = pd.read_csv('BX-CSV/BX-Users.csv', sep=';', error_bad_lines=False, encoding="latin-1")
users.columns = ['userID', 'Location', 'Age']
ratings = pd.read_csv('BX-CSV/BX-Book-Ratings.csv', sep=';', error_bad_lines=False, encoding="latin-1")
ratings.columns = ['userID', 'ISBN', 'bookRating']

print('-----------------------------------------')

print(colored('KNN是一个用来基于共同图书评分以发现相似读者间聚类状况的机器学习算法，并且可以基于距离最近的 k 个邻居的平均评分来进行预测', 
              'red', attrs=['reverse', 'blink']))