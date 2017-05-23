import argparse

import six


def sumrange(n):
    result = 0
    for value in six.moves.xrange(n):
        result += value

    return result


def get_num_procs(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--num-procs', dest='num_procs',
                        type=int, default=4)
    args = parser.parse_args()
    return args.num_procs
