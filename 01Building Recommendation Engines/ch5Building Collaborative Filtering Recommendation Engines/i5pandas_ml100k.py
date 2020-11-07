import i4ml100k
import numpy as np
import pandas as pd
import sklearn
from sklearn.cross_validation import train_test_split

# df = i4ml100k.load_csv_to_df()

df = pd.read_csv('../data/ml100k_small.csv', sep=",", header=0)


n_users = df.UserID.unique().shape[0]
n_items = df['ItemID'].unique().shape[0]

print('total number of unique users in the data:', n_users)
print('total number of unique movies in the data', n_items)

print('Create a zero value matrix of size (n_users x n_items)\
 to store the ratings in the cell of the matrix ratings')
ratings = np.zeros((n_users, n_items))

for row in df.itertuples():
    # if row[0] < 5:
    #     print('row=',row, 'r[1]=', row[1], row[2], row[3])
    ratings[row[1] -1, row[2] - 1] = row[3]

print(type(ratings),ratings.shape,'\n\n', ratings)

# 稀疏度
sparsity = float(len(ratings.nonzero()[0]))
sparsity /= (ratings.shape[0] * ratings.shape[1])
sparsity *= 100
print('Sparsity: {:4.2f}%'.format(sparsity))

ratings_train, ratings_test = train_test_split(ratings,test_size=0.33, random_state=42)
print(ratings_test.shape)

# user-based similarity-------------------------------------
dist_out = 1-sklearn.metrics.pairwise.cosine_distances(ratings_train)
print(type(dist_out), dist_out.shape)

user_pred = dist_out.dot(ratings_train) / np.array([np.abs(dist_out).sum(axis=1)]).T

from sklearn.metrics import mean_squared_error
def get_mse(pred, actual):
    # Ignore nonzero terms.
    pred = pred[actual.nonzero()].flatten()
    actual = actual[actual.nonzero()].flatten()
    return mean_squared_error(pred, actual)

print(get_mse(user_pred, ratings_train), get_mse(user_pred, ratings_test))
