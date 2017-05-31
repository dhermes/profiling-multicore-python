import threading

import six

import shared


def main():
    num_threads = shared.get_num_workers(
        'Run threading test.', 'num_threads')
    to_sum = 2**26

    for cpu_id in six.moves.xrange(num_threads):
        thread = threading.Thread(
            target=shared.sumrange, args=(cpu_id, to_sum))
        thread.start()


if __name__ == '__main__':
    main()
