import i4ml100k
import numpy as np
import pandas as pd

# df = i4ml100k.load_csv_to_df()
path = '../data/ml100k_small.csv'
df = pd.read_csv(path, sep=",", header=0)


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