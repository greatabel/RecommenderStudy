import pandas as pd
import matplotlib.pyplot as plt

def load_csv_to_df(path="../data/ml-100k_udata.csv"):
    df = pd.read_csv(path, sep="\t", names=['UserID', 'ItemID', 'Rating', 'Timestamp'])
    return df

if __name__ == "__main__":
    df = load_csv_to_df()
    print('type(df)=', type(df))
    print('df.head()=', df.head())
    print('df.columns=', df.columns)
    print('df.shape=', df.shape)

    plt.hist(df['Rating'])
    plt.show()