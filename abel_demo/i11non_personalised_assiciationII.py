import  pandas as pd
import  numpy as np


from termcolor import colored
# https://medium.com/@tomar.ankur287/non-personalised-recommender-system-in-python-42921cd6f971

ratings = pd.read_csv("movies_ratings_tags_csv/ratings.csv",encoding="ISO-8859-1")
movies = pd.read_csv("movies_ratings_tags_csv/movies.csv",encoding="ISO-8859-1")
tags = pd.read_csv("movies_ratings_tags_csv/tags.csv",encoding="ISO-8859-1")

movie_association = pd.DataFrame(columns=['movieId','movieId1','association'])
distinct_movies = np.unique(ratings['movieId'])
print('distinct_movies[150:200]=', distinct_movies[150:200])


print(colored('enter movie ID for analysis : 260', 'green', attrs=['reverse', 'blink']))
movieID = 260

# movie_index = distinct_movies.tolist().index(movieID)
# print('movie_index=', movie_index, type(movie_index))


movie_data= ratings[ratings['movieId'] == movieID]
print(movie_data.head(10), len(movie_data))
j = 1
for movie1 in distinct_movies:
        
    movie1_data = ratings[ratings['movieId']==movie1]
    distinct_cust = len(np.unique(movie_data['userId']))
    distinct_cust1 = len(np.unique(movie1_data['userId']))
    movie2_data = movie1_data[movie1_data['userId'].isin(np.unique([movie_data['userId']]))]
    distinct_cust_common = len(np.unique(movie2_data['userId']))
    fraction_common_cust=(float(distinct_cust_common)*len(np.unique(ratings['userId']))) \
                            /(float(distinct_cust)*float(distinct_cust1))
    
    movie_temp =pd.DataFrame(columns=['movieId','movieId1','association'])
    
    movie_temp = movie_temp.append({
    "movieId": movieID,
    "movieId1":  movie1,
    "association":  fraction_common_cust      
    }, ignore_index=True)
    
    
    movie_association = movie_association.append(movie_temp, ignore_index=True)
    if j%500 == 0:
        print ("j=", j)
    j = j+1

movie_association = movie_association.sort_values(['association'], ascending=False)
print(movie_association.head(100))
