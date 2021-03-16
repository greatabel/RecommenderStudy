import numpy as np
import pandas as pd
import math
from  common import write_to_file, groupby


 
def signature_bit(data, planes):
    """
    LSH signature generation using random projection
    Returns the signature bits for two data points.
    The signature bits of the two points are different
    only for the plane that divides the two points.
    """
    sig = 0
    for p in planes:
        sig <<=  1      
        if np.dot(data, p) >= 0:
            sig |= 1
    return sig


def bitcount(n):
    """
    gets the number of bits set to 1
    """
    count = 0
    while n:
        count += 1
        n = n & (n-1)
    return count
 
def length(v):
    """returns the length of a vector"""
    return math.sqrt(np.dot(v, v))


def cosine(data, seed):
    df = pd.DataFrame(data, columns=["userid", "movieid", "rating"])
    print(df)
    r = df.pivot(*df.columns)
    df_list = r.values.tolist()
    print(df_list)
    print('-'*10, 'step0')
    dim = 2763      # dimension of data points (# of features)
    bits = 100    # number of bits (planes) per signature

    user_pair = []
    for u1, v1 in enumerate(df_list):
        pt1 = np.asarray(v1, dtype=np.float32)
        for u2, v2 in enumerate(df_list):
            pt2 = np.asarray(v2, dtype=np.float32)
            # print(pt1, pt2, '#'*5)
            # reference planes as many as bits (= signature bits)
            ref_planes = np.random.randn(bits, dim)

            # signature bits for two data points
            sig1 = signature_bit(pt1, ref_planes)
            sig2 = signature_bit(pt2, ref_planes)

            # Calculates exact angle difference
            cosine = np.dot(pt1,pt2)/length(pt1)/length(pt2)
            exact = 1 - math.acos(cosine)/math.pi

            # Calculates angle difference using LSH based on cosine distance
            # It's using signature bits' count
            cosine_hash = 1 - bitcount(sig1^sig2)/bits
            if u1 < u2 and cosine_hash > 0.67:
                print(u1, u2, cosine_hash)
                user_pair.append(str(u1)+', '+str(u2))
    write_to_file('cs.txt', user_pair)