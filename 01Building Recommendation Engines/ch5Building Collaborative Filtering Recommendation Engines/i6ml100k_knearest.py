import i4ml100k
import numpy as np
import pandas as pd
import sklearn
from sklearn.cross_validation import train_test_split

df = i4ml100k.load_csv_to_df()

# df = pd.read_csv('../data/ml100k_small.csv', sep=",", header=0)


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



ratings_train, ratings_test = train_test_split(ratings,test_size=0.33, random_state=42)
print(ratings_test.shape)

from sklearn.metrics import mean_squared_error
def get_mse(pred, actual):
    # Ignore nonzero terms.
    pred = pred[actual.nonzero()].flatten()
    actual = actual[actual.nonzero()].flatten()
    return mean_squared_error(pred, actual)

#--------------------------------------------

k=5
from sklearn.neighbors import NearestNeighbors

#define  NearestNeighbors object by passing k and the similarity method as parameters.
neigh = NearestNeighbors(k,'cosine')

#fit the training data to the nearestNeighbor object
neigh.fit(ratings_train)

#calculate the top5 similar users for each user and their similarity  values, i.e. the distance values between each pair of users.
top_k_distances,top_k_users = neigh.kneighbors(ratings_train, return_distance=True)

top_k_distances.shape
top_k_users.shape
top_k_users[0]
user_pred_k = np.zeros(ratings_train.shape)
for i in range(ratings_train.shape[0]):
    user_pred_k[i,:] =   top_k_distances[i].T.dot(ratings_train[top_k_users][i])/np.array([np.abs(top_k_distances[i].T).sum(axis=0)]).T




print('#'*10, get_mse(user_pred_k, ratings_train), get_mse(user_pred_k, ratings_test))

#Since we have to calculate the similarity between movies, we use movie count as k instead of user count
k = ratings_train.shape[1]
neigh = NearestNeighbors(k,'cosine')
#we fit the transpose of the rating matrix to the Nearest Neighbors object
neigh.fit(ratings_train.T)
#calcualte the cosine similarity distance between each movie pairs
top_k_distances,top_k_users = neigh.kneighbors(ratings_train.T, return_distance=True)
top_k_distances.shape

item_pred = ratings_train.dot(top_k_distances) / np.array([np.abs(top_k_distances).sum(axis=1)])


print('@'*10, get_mse(item_pred, ratings_train),get_mse(item_pred,ratings_test))


