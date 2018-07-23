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

rating_count = pd.DataFrame(ratings.groupby('ISBN')['bookRating'].count())
h = rating_count.sort_values('bookRating', ascending=False).head()
print(colored('rating_count =>', 
              'red', attrs=['reverse', 'blink']))
print(h)
serie = h['bookRating']
ibsn_list = serie.axes[0].tolist()
print('ibsn_list=>', ibsn_list)

most_rated_books = pd.DataFrame(ibsn_list, index=np.arange(5), columns = ['ISBN'])
most_rated_books_summary = pd.merge(most_rated_books, books, on='ISBN')
pd.set_option('display.max_colwidth', -1)
print(most_rated_books_summary)

