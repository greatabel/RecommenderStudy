import pandas as pd


path = "../data/ml-100k_udata.csv"

df = pd.read_csv(path, sep="\t", names=['UserID', 'ItemID', 'Rating', 'Timestamp'])
print('type(df)=', type(df))
print('df.head()=', df.head())
print('df.columns=', df.columns)
print('df.shape=', df.shape)