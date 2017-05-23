import argparse
import threading

import six


def sumrange(n):
    result = 0
    for value in six.moves.xrange(n):
        result += value

    print(result)


def get_num_procs():
    parser = argparse.ArgumentParser(
        description='Run multiprocessing test.')
    parser.add_argument('--num-procs', dest='num_procs',
                        type=int, default=4)
    args = parser.parse_args()
    return args.num_procs


def main():
    nt = 2
    n = 2**28

    threads = []
    for i in six.moves.xrange(nt):
        t = threading.Thread(target=sumrange, args=(n,))
        threads.append(t)
        t.start()


if __name__ == '__main__':
    main()
