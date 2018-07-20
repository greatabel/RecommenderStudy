# https://stackoverflow.com/questions/18424228/cosine-similarity-between-2-number-lists
import math

def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy / math.sqrt(sumxx*sumyy)

if __name__ == "__main__":
    v1,v2 = [3, 2.5, 3.5, 3.5, 3.0, 2.5], [2.0, 3.0, 4.0, 3.0, 3.0, 2.0]
    print(v1, v2, cosine_similarity(v1,v2))