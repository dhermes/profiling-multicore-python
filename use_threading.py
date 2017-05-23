import threading

import six

import shared


def sumrange(n):
    print(shared.sumrange(n))


def main():
    num_threads = shared.get_num_procs('Run threading test.')
    to_sum = 2**26
    args = (to_sum,)

    for i in six.moves.xrange(num_threads):
        t = threading.Thread(target=sumrange, args=args)
        t.start()


if __name__ == '__main__':
    main()
