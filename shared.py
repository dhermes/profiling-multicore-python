import argparse
import os

import six


def setaffinity(cpu_id):
    if not six.PY3:
        raise EnvironmentError(
            'os.sched_setaffinity only exists in Python 3')

    # NOTE: "Current process" won't be the same as ``os.getpid()``
    #       for Python threads. These will actually correspond to the
    #       "thread ID" (Python used native ``pthread``-s when possible).
    pid = 0  # Zero == Current Process
    os.sched_setaffinity(pid, [cpu_id])


def sumrange(cpu_id, n, pin_cpu):
    if pin_cpu:
        setaffinity(cpu_id)

    result = 0
    for value in six.moves.xrange(n):
        result += value

    print(result)


def get_workers_info(description, name):
    parser = argparse.ArgumentParser(description=description)
    flag = '--' + name.replace('_', '-')
    parser.add_argument(flag, dest=name,
                        type=int, default=4)
    pin_cpu_help = (
        'Indicates if each process/thread should be pinned '
        'to a given CPU.')
    parser.add_argument(
        '--pin-cpu', dest='pin_cpu',
        action='store_true', help=pin_cpu_help)

    args = parser.parse_args()
    num_workers = getattr(args, name)

    return num_workers, args.pin_cpu
