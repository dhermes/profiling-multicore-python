import argparse

import six


def sumrange(n):
    result = 0
    for value in six.moves.xrange(n):
        result += value

    return result


def get_num_workers(description, name):
    parser = argparse.ArgumentParser(description=description)
    flag = '--' + name.replace('_', '-')
    parser.add_argument(flag, dest=name,
                        type=int, default=4)

    args = parser.parse_args()
    return getattr(args, name)
