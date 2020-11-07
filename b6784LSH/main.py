import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='proper argument to run experiment')
    parser.add_argument('--d', type=str, default='/',
                        help="Data file path")
    parser.add_argument('--s', type=int, default=2020,
                        help='Random seed (by using np.random.seed(int)) ')
    parser.add_argument('--m', type=str, default='js',
                        help='Similarity measure (js / cs / dcs)')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    print('是否使用GPU:', args.d, args.s, args.m)



if __name__ == "__main__":
    main()
    # python3 main.py -d /very/long/path/to/data.npy -s 2020 -m js