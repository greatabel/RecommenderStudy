import pandas as pd
import time
# import redis
# from flask import current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

# http://blog.untrod.com/2016/06/simple-similar-products-recommendation-engine-in-python.html
data_source = 'sample-data.csv'


def train():
    start = time.time()
    ds = pd.read_csv(data_source)
    print("Training data ingested in %s seconds." % (time.time() - start))
    
    """
    Train the engine.

    Create a TF-IDF matrix of unigrams, bigrams, and trigrams
    for each product. The 'stop_words' param tells the TF-IDF
    module to ignore common english words like 'the', etc.

    Then we compute similarity between all products using
    SciKit Leanr's linear_kernel (which in this case is
    equivalent to cosine similarity).

    Iterate through each item's similar items and store the
    100 most-similar. Stops at 100 because well...  how many
    similar products do you really need to show?

    Similarities and their scores are stored in redis as a
    Sorted Set, with one set for each item.

    :param ds: A pandas dataset containing two fields: description & id
    :return: Nothin!
    """
    tf = TfidfVectorizer(analyzer='word',
                             ngram_range=(1, 3),
                             min_df=0,
                             stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['description'])

    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    for idx, row in ds.iterrows():
            similar_indices = cosine_similarities[idx].argsort()[:-100:-1]
            similar_items = [(cosine_similarities[idx][i], ds['id'][i])
                             for i in similar_indices]

            # First item is the item itself, so remove it.
            # This 'sum' is turns a list of tuples into a single tuple:
            # [(1,2), (3,4)] -> (1,2,3,4)
            flattened = sum(similar_items[1:], ())
            print(row['id'], '-'*10, flattened)
            

def main():
    train()

if __name__ == "__main__":
    main()