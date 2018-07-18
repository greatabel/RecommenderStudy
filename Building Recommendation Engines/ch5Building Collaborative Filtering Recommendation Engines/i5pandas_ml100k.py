import i4ml100k

df = i4ml100k.load_csv_to_df()
n_users = df.UserID.unique().shape[0]
n_items = df['ItemID'].unique().shape[0]

print('total number of unique users in the data:', n_users)
print('total number of unique movies in the data', n_items)