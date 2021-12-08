import numpy as np
import pandas as pd


def groupby(X): 
    # delete rating column
    b = np.delete(X, -1, axis=1)

    df = pd.DataFrame(b, columns=["key", "val"])
    return df.groupby("key").val.apply(pd.Series.tolist)


def write_to_file(filepath, my_list):
    with open(filepath, "w") as f:
        for item in my_list:
            f.write("%s\n" % item)