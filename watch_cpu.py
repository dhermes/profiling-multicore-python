import argparse
import subprocess
import time


DEFAULT_INTERVAL = 1.0


def get_args():
    parser = argparse.ArgumentParser(
        description='Profile CPU while doing a computation.')
    parser.add_argument(
        '--total-intervals', dest='total_intervals',
        type=int, required=True,
        help='Total number of intervals to profile for.')
    parser.add_argument(
        '--interval', type=float, default=DEFAULT_INTERVAL,
        help='The sample interval during profiling.')
    script_help = (
        'The Python script to execute for profiling. All unused '
        'arguments will be passed to the script.')
    parser.add_argument(
        '--script', required=True, help=script_help)

    return parser.parse_known_args()


def main():
    args, unknown = get_args()

    # https://stackoverflow.com/a/11316397/1068170
    # https://stackoverflow.com/a/41433401/1068170
    cmd1 = (
        'python',
        'profile_cpu.py',
        '--total-intervals', str(args.total_intervals),
        '--interval', str(args.interval),
    )
    proc1 = subprocess.Popen(cmd1)

    # Do some profiling before starting the computation.
    time.sleep(3)
    cmd2 = ('python', args.script) + tuple(unknown)
    proc2 = subprocess.Popen(cmd2)

    # Keep this process alive until both subprocesses are done,
    # but don't block on either one.
    while proc1.poll() is None or proc2.poll() is None:
        time.sleep(1)


if __name__ == '__main__':
    main()
