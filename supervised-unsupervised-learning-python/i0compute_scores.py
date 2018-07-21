import json
import numpy as np


def euclidean_score(dataset, user1, user2):
    ""

def pearson_score(dataset, user1, user2):
    ""

if __name__=='__main__':
    ratings_file = 'ratings.json'
    with open(ratings_file, 'r') as f:
        data = json.loads(f.read())

    user1 = 'David Smith'
    user2 = 'Brenda Peterson'


    print("\nEuclidean score:")
    print(euclidean_score(data, user1, user2))

    print("\nPearson score:")
    print(pearson_score(data, user1, user2))