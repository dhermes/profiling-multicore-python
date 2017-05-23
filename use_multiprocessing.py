import argparse
import multiprocessing

import six


def sumrange(n):
    result = 0
    for value in six.moves.xrange(n):
        result += value

    return result


def get_num_procs():
    parser = argparse.ArgumentParser(
        description='Run multiprocessing test.')
    parser.add_argument('--num-procs', dest='num_procs',
                        type=int, default=4)
    args = parser.parse_args()
    return args.num_procs


def main():
    np = get_num_procs()
    p = multiprocessing.Pool(processes=np)
    n = 2**28
    inputs = [n] * np
    result = p.map(sumrange, inputs)
    print(result)


if __name__ == '__main__':
    main()
