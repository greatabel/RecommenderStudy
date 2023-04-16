#!/usr/bin/env python
# coding: utf-8

# In[74]:


# Sports_and_Outdoors.csv
# from https://nijianmo.github.io/amazon/index.html#code
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

# Load the Amazon review dataset into a pandas dataframe
import pandas as pd
import matplotlib.pyplot as plt


from sklearn.model_selection import KFold



# In[75]:
#数据集太大，我放在需求文件夹了，只留下sample

df = pd.read_csv('Sports_and_Outdoors.csv', header=None, names=['product_id', 'user_id', 'rating', 'timestamp'])


# In[76]:


df.head()


# In[77]:


print("Length of the DataFrame:", len(df))


# In[78]:


df = df.drop('timestamp', axis=1) #Dropping timestamp

df_copy = df.copy(deep=True)


# In[79]:


# Convert the user_id column from string to integer
# Map the user_id column to integers
df['user_id'] = pd.factorize(df['user_id'])[0]

df['product_id'] = pd.factorize(df['product_id'])[0]


# In[80]:


#Check Data types
df.dtypes


# In[81]:


df.head()


# In[82]:


# Plot the distribution of user ratings
plt.hist(df['rating'], bins=[0.5,1.5,2.5,3.5,4.5,5.5])
plt.title('Distribution of User Ratings')
plt.xlabel('Rating')
plt.ylabel('Count')
plt.show()

# Plot the distribution of product ratings
product_rating_counts = df.groupby('product_id')['rating'].count().values
plt.hist(product_rating_counts, bins=range(1,50))
plt.title('Distribution of Product Rating Counts')
plt.xlabel('Number of Ratings per Product')
plt.ylabel('Count')
plt.show()


# In[83]:


# Calculate the average rating for each product
average_rating = df.groupby('product_id')['rating'].mean()
# Calculate the count of ratings for each product
count_rating = df.groupby('product_id')['rating'].count()

# Create a dataframe with calculated average and count of ratings
product_ratings = pd.DataFrame({'Average Rating':average_rating, 'Rating Count':count_rating})

# Sort the dataframe by average of ratings
product_ratings_sorted = product_ratings.sort_values(by='Average Rating', ascending=False)

# Plot the distribution of average product ratings
plt.hist(product_ratings_sorted['Average Rating'], bins=np.arange(2.5, 5.1, 0.1))
plt.title('Distribution of Average Product Ratings')
plt.xlabel('Average Rating')
plt.ylabel('Count')
plt.show()

# Plot the distribution of product rating counts
plt.hist(product_ratings_sorted['Rating Count'], bins=range(1, 100, 5))
plt.title('Distribution of Product Rating Counts')
plt.xlabel('Number of Ratings per Product')
plt.ylabel('Count')
plt.show()

# Plot the top 20 products by average rating
product_ratings_top20 = product_ratings_sorted.head(20)
product_ratings_top20.plot(kind='bar', y='Average Rating', legend=False)
plt.title('Top 20 Products by Average Rating')
plt.xlabel('Product ID')
plt.ylabel('Average Rating')
plt.show()


# In[111]:


counts = df['user_id'].value_counts()
df_final = df[df['user_id'].isin(counts[counts >= 50].index)]

print('The number of observations in the final data =', len(df_final))
print('Number of unique USERS in the final data = ', df_final['user_id'].nunique())
print('Number of unique PRODUCTS in the final data = ', df_final['product_id'].nunique())


# In[112]:


# from surprise import Dataset
# from surprise import Reader
# from surprise import SVD
# from surprise.model_selection import cross_validate
# from surprise.model_selection import train_test_split

# df_copy = df_final.copy(deep=True)
# # Convert the user_id column from string to integer and map to integers
# # df['user_id'] = pd.factorize(df['user_id'])[0]
# # df['product_id'] = pd.factorize(df['product_id'])[0]

# # Define the scale of the rating values
# reader = Reader(rating_scale=(1, 5))

# # Load the dataset into Surprise format
# data = Dataset.load_from_df(df[['user_id', 'product_id', 'rating']], reader)

# # Split the dataset into training and testing sets
# trainset, testset = train_test_split(data, test_size=.25)

# # Define the SVD model with 50 latent factors and regularization parameter of 0.01
# model = SVD(n_factors=50, reg_all=0.01)

# # Train the model on the training set
# model.fit(trainset)

# # Evaluate the model using RMSE and MAE metrics
# results = cross_validate(model, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# # Print the average RMSE and MAE across the 5 folds
# print('Average RMSE:', results['test_rmse'].mean())
# print('Average MAE:', results['test_mae'].mean())

# # Predict the ratings for the test set
# predictions = model.test(testset)

# # Print the first 10 predicted ratings
# for pred in predictions[:10]:
#     print('User:', pred.uid, 'Product:', pred.iid, 'Rating:', pred.est)




# In[113]:


# Calculate some basic statistics about the dataset

# Convert the 'user_id' column to a string data type
# df['user_id'] = df['user_id'].astype(str)

n_users = df['user_id'].nunique()
n_products = df['product_id'].nunique()
print('Number of unique users:', n_users)
print('Number of unique products:', n_products)
print('Average rating:', np.mean(df['rating']))


# In[114]:


# Aggregate the duplicate ratings by taking the mean
df_final_agg = df_final.groupby(['user_id', 'product_id'])['rating'].mean().reset_index()

# Pivot the dataframe to create the interaction matrix
final_ratings_matrix = df_final_agg.pivot(index='user_id', columns='product_id', values='rating').fillna(0)

# Print the shape and density of the matrix
print('Shape of final_ratings_matrix: ', final_ratings_matrix.shape)

given_num_of_ratings = np.count_nonzero(final_ratings_matrix)
print('given_num_of_ratings = ', given_num_of_ratings)

possible_num_of_ratings = final_ratings_matrix.shape[0] * final_ratings_matrix.shape[1]
print('possible_num_of_ratings = ', possible_num_of_ratings)

density = (given_num_of_ratings/possible_num_of_ratings)
density *= 100
print ('density: {:4.2f}%'.format(density))

final_ratings_matrix.head()


# In[115]:


from sklearn.metrics.pairwise import cosine_similarity

from sklearn.metrics import mean_squared_error



def similar_users(user_index, interactions_matrix):
    similarity = []
    for user in range(0, interactions_matrix.shape[0]):
        #finding cosine similarity between the user_index and each user
        sim = cosine_similarity([interactions_matrix.loc[user_index]], [interactions_matrix.loc[user]])
        #Appending the user and the corresponding similarity score with user_index as a tuple
        similarity.append((user, sim))
        
    similarity.sort(key=lambda x: x[1], reverse=True)
    most_similar_users = [Tuple[0] for Tuple in similarity] 
    #Extract the user from each tuple in the sorted list
    similarity_score = [Tuple[1] for Tuple in similarity]   
    ##Extracting the similarity score from each tuple in the sorted list
   
    #Remove the original user and its similarity score and keep only other similar users 
    most_similar_users.remove(user_index)
    similarity_score.remove(similarity_score[0])
       
    return most_similar_users, similarity_score


# In[116]:


#Calculate the average rating for each product 
average_rating = df_final.groupby(['product_id']).mean().rating
print(average_rating.head())
#Calculate the count of ratings for each product
count_rating = df_final.groupby(['product_id']).count().rating

#Create a dataframe with calculated average and count of ratings
final_rating = pd.DataFrame(pd.concat([average_rating,count_rating], axis = 1))
final_rating.columns=["Average Rating", "Ratings Count"]

#Sort the dataframe by average of ratings
final_rating = final_rating.sort_values(by='Average Rating', ascending=False)

final_rating.head()


# In[117]:


def my_top_n_products(final_rating, n, min_interaction):
    

    recommendations = final_rating[final_rating['Ratings Count'] >= min_interaction]
    

    recommendations = recommendations.sort_values(by='Average Rating', ascending=False)
    
    return recommendations.index[:n]


# In[118]:


list(my_top_n_products(final_rating, 5, 50))


# In[ ]:





# In[110]:







# In[ ]:





# In[ ]:





# In[ ]:




