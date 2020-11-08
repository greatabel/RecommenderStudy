import numpy as np
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='proper argument to run experiment')
    parser.add_argument('-d', type=str, default='/',
                        help="Data file path")
    parser.add_argument('-s', type=int, default=2020,
                        help='Random seed (by using np.random.seed(int)) ')
    parser.add_argument('-m', type=str, default='js',
                        help='Similarity measure (js / cs / dcs)')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    print('args:', args.d, args.s, args.m)
    data = np.load(args.d)
    print(data, data.shape, type(data))
    # generate small dataset for rapid test
    # np.save('small_user_movie_rating.npy', data[0:10000])
    



if __name__ == "__main__":
    main()
    # real test
    # python3 main.py -d /Users/abel/Downloads/spare_time/b6784_900_recommand_doing/user_movie_rating.npy  -s 2020 -m js

    # small test, just for rapid prototype
    # python3 main.py -d small_user_movie_rating.npy  -s 2020 -m js