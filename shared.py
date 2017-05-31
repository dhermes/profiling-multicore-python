import argparse

import six


def sumrange(cpu_id, n):
    # NOTE: `cpu_id` is unused for now but **will** be used to set
    #       CPU affinity.
    result = 0
    for value in six.moves.xrange(n):
        result += value

    print(result)


def get_num_workers(description, name):
    parser = argparse.ArgumentParser(description=description)
    flag = '--' + name.replace('_', '-')
    parser.add_argument(flag, dest=name,
                        type=int, default=4)

    args = parser.parse_args()
    return getattr(args, name)
