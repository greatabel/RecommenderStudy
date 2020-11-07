import pandas as pd
import numpy as np
import scipy
import sklearn
from termcolor import colored


path = "../data/anonymous-msweb.test"
raw_data = pd.read_csv(path,header=None,skiprows=7)

#creating user profile
user_activity = raw_data.loc[raw_data[0] != "A"]
print('type(user_activity)=', type(user_activity))
user_activity.columns = ['category','value','vote','desc','url']
user_activity = user_activity[['category','value']]

# Attribute (A): This is the description of the website area
# Case (C): This is the case for each user, containing its ID
# Vote (V): This is the vote lines for the case
print(user_activity.groupby('category').count())
print(user_activity.head(15))

print(colored('- . -- . -- . -- . -- . -', 'red', attrs=['reverse', 'blink']))
w_count = len(user_activity.loc[user_activity['category'] == 'V'].value.unique())
u_count = len(user_activity.loc[user_activity['category'] == 'C'].value.unique())

print('get unique webid count:', w_count)
print('get unique users count:', u_count)



print(colored('create a user-item-rating matrix ', 'red', attrs=['reverse', 'blink']))
tmp = 0
nextrow = False
print(user_activity.index)
lastindex = user_activity.index[len(user_activity) -1]

for index,row in user_activity.iterrows():
    if(index <= lastindex ):
        if(user_activity.loc[index,'category'] == "C"):
            tmp = 0
            #add += 1
            #user_activity.loc[index,'chunk'] += add
            userid = user_activity.loc[index,'value']
            user_activity.loc[index,'userid'] = userid
            user_activity.loc[index,'webid'] = userid
            tmp = userid
            nextrow = True            
        elif(user_activity.loc[index,'category'] != "C" and nextrow == True):
                #user_activity.loc[index,'chunk'] += add
                webid = user_activity.loc[index,'value']
                user_activity.loc[index,'webid'] = webid
                user_activity.loc[index,'userid'] = tmp
                if(index != lastindex and user_activity.loc[index+1,'category'] == "C"):
                    nextrow = False
                    caseid = 0

print(user_activity.head(15))

user_activity = user_activity[user_activity['category'] == "V" ]
user_activity = user_activity[['userid','webid']]
# user_activity_sort = user_activity.sort('webid', ascending=True)
user_activity_sort = user_activity.sort_values(by=['webid'], ascending=True)

# “Then we add a new column, 'rating' to the user_activity data frame which contains only 1”
sLength = len(user_activity_sort['webid'])
user_activity_sort['rating'] = pd.Series(np.ones((sLength,)), index=user_activity.index)
print(user_activity_sort.head(15))
ratmat = user_activity_sort.pivot(index='userid', columns='webid', values='rating').fillna(0)
ratmat = ratmat.to_dense().as_matrix()



print(colored('item profile generation ', 'blue', attrs=['reverse', 'blink']))
items = raw_data.loc[raw_data[0] == "A"]
items.columns = ['record','webid','vote','desc','url']
items = items[['webid','desc']]
items2 = items[items['webid'].isin(user_activity['webid'].tolist())]
items_sort = items2.sort_values(by=['webid'], ascending=True)
print(items_sort.head(15))


from sklearn.feature_extraction.text import TfidfVectorizer
v = TfidfVectorizer(stop_words ="english",max_features = 100,ngram_range= (0,3),sublinear_tf =True)
x = v.fit_transform(items_sort['desc'])
itemprof = x.todense()


#dot product
from scipy import linalg, dot
userprof = dot(ratmat,itemprof)/linalg.norm(ratmat)/linalg.norm(itemprof)

import sklearn.metrics
similarityCalc = sklearn.metrics.pairwise.cosine_similarity(userprof, itemprof, dense_output=True)
#covert the rating to binary format
final_pred= np.where(similarityCalc>0.6, 1, 0)
indexes_of_user = np.where(final_pred[213] == 1)
print('user 213 recommend:', indexes_of_user)