import multiprocessing

import six

import shared


def main():
    num_procs = shared.get_num_workers(
        'Run multiprocessing test.', 'num_procs')
    to_sum = 2**28

    for cpu_id in six.moves.xrange(num_procs):
        process = multiprocessing.Process(
            target=shared.sumrange, args=(cpu_id, to_sum))
        process.start()


if __name__ == '__main__':
    main()
