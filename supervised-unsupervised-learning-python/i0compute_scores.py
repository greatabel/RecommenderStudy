import json
import numpy as np


def find_similar_users(dataset, user, num_users):
    if user not in dataset:
        raise TypeError('Cannot find ' + user + ' in the dataset')
        
if __name__=='__main__':
    ratings_file = 'ratings.json'
    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    user = 'David Smith'
    print('\nUsers similar to ' + user + ':\n')
    similar_users = find_similar_users(data, user, 3)