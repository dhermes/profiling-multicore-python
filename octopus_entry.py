import subprocess
import time


def main():
    # https://stackoverflow.com/a/11316397/1068170
    # https://stackoverflow.com/a/41433401/1068170
    cmd1 = ('python', 'profile_cpu.py', '--total-intervals', '12')
    proc1 = subprocess.Popen(cmd1)

    # Do some profiling before starting the computation.
    time.sleep(3)
    cmd2 = ('python', 'use_multiprocessing.py', '--num-procs', '2')
    proc2 = subprocess.Popen(cmd2)

    # Keep this process alive until both subprocesses are done,
    # but don't block on either one.
    while proc1.poll() is None or proc2.poll() is None:
        time.sleep(1)


if __name__ == '__main__':
    main()
