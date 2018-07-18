import pandas as pd
import numpy as np
import scipy
import sklearn

path = "../data/anonymous-msweb.test"
raw_data = pd.read_csv(path,header=None,skiprows=7)

#creating user profile
user_activity = raw_data.loc[raw_data[0] != "A"]
user_activity.columns = ['category','value','vote','desc','url']
user_activity = user_activity[['category','value']]

# Attribute (A): This is the description of the website area
# Case (C): This is the case for each user, containing its ID
# Vote (V): This is the vote lines for the case
print(user_activity.groupby('category').count())