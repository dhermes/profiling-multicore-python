import argparse
import ctypes
import os
import threading
try:
    import win32api
    import win32process
except ImportError:
    win32api = None
    win32process = None

import six


try:
    LIBC = ctypes.cdll.LoadLibrary('libc.so.6')
except WindowsError:
    LIBC = None


def win_setaffinity(cpu_id):
    # H/T: https://pypi.python.org/pypi/affinity/0.1.0
    proc_mask = 2**cpu_id

    curr_py_thread = threading.current_thread()
    if curr_py_thread.name == 'MainThread':
        curr_proc = win32process.GetCurrentProcess()
        win32process.SetProcessAffinityMask(curr_proc, proc_mask)
    else:
        curr_win_thread = win32api.GetCurrentThread()
        win32process.SetThreadAffinityMask(curr_win_thread, proc_mask)


def libc_setaffinity(pid, cpu_id):
    # H/T: http://developers-club.com/posts/141181/
    # BEGIN: syscall setup (should be globals but meh).
    cpu_set_t = ctypes.c_size_t
    cpu_set_t_ptr = ctypes.POINTER(cpu_set_t)
    # From: https://linux.die.net/man/2/sched_getaffinity
    # int sched_setaffinity(pid_t pid, size_t cpusetsize,
    #                       cpu_set_t *mask);
    setaffinity_syscall = LIBC.sched_setaffinity
    setaffinity_syscall.argtypes = [
        ctypes.c_int,  # pid_t,
        ctypes.c_size_t,  # size_t
        cpu_set_t_ptr,  # *cpu_set_t
    ]
    #   END: syscall setup

    mask = cpu_set_t(2**cpu_id)
    cpusetsize = ctypes.sizeof(cpu_set_t)
    if setaffinity_syscall(pid, cpusetsize, mask) < 0:
        raise OSError('Failed sched_setaffinity system call')


def setaffinity(cpu_id):
    # NOTE: "Current process" won't be the same as ``os.getpid()``
    #       for Python threads. These will actually correspond to the
    #       "thread ID" (Python used native ``pthread``-s when possible).
    pid = 0  # Zero == Current Process
    if six.PY3:
        os.sched_setaffinity(pid, [cpu_id])
    elif LIBC is not None:
        libc_setaffinity(pid, cpu_id)
    elif win32process is not None:
        win_setaffinity(cpu_id)
    else:
        raise NotImplementedError('Cannot setaffinity on current platform')


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
