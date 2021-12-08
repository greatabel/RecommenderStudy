import numpy as np
import pandas as pd
from  my_minhash import MinHash
from  common import write_to_file, groupby





def jaccard(data, seed):
    m_dict = {}
    r = groupby(data)
    print('-'*10, 'step0')
    for i, v in r.items():
        # print('index: ', i, 'value: ', v)
        m = MinHash(seed=seed)
        for movie in v:
            m.add(str(movie).encode('utf8'))
        m_dict[i] = m
    print('-'*20, 'jaccard step1 finished', len(m_dict))
    user_pair = []
    i = 0
    for u1, m1 in m_dict.items():
        i += 1
        if i % 1000 == 0:
            print('i=', i)
        for u2, m2 in m_dict.items():
            j = m1.jaccard(m2)
            if j > 0.3:
            # if j > 0.5:
                if u1 < u2:
                    print(u1, u2, j)
                    user_pair.append(str(u1)+', '+str(u2))
    write_to_file('js.txt', user_pair)
