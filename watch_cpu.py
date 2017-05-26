import argparse
import subprocess
import time


def get_args():
    parser = argparse.ArgumentParser(
        description='Profile CPU while doing a computation.')
    parser.add_argument(
        '--total-intervals', dest='total_intervals',
        type=int, required=True,
        help='Total number of intervals to profile for.')
    parser.add_argument(
        '--interval', type=float,
        help='The sample interval during profiling.')
    script_help = (
        'The Python script to execute for profiling. All unused '
        'arguments will be passed to the script.')
    parser.add_argument(
        '--script', required=True, help=script_help)
    filename_help = (
        'The filename to save the plot into. If not provided, the plot '
        'will just be displayed interactively.')
    parser.add_argument('--filename', help=filename_help)
    parser.add_argument(
        '--data-id', dest='data_id',
        help='Identifier for the profile data when being saved.')

    return parser.parse_known_args()


def start_profiler(args):
    cmd = (
        'python',
        'profile_cpu.py',
        '--total-intervals', str(args.total_intervals),
    )
    if args.interval is not None:
        cmd += ('--interval', str(args.interval))
    if args.filename is not None:
        cmd += ('--filename', args.filename)
    if args.data_id is not None:
        cmd += ('--data-id', args.data_id)
    return subprocess.Popen(cmd)


def start_script(args, unknown):
    cmd = ('python', args.script) + tuple(unknown)
    return subprocess.Popen(cmd)


def main():
    args, unknown = get_args()
    # https://stackoverflow.com/a/11316397/1068170
    # https://stackoverflow.com/a/41433401/1068170
    proc1 = start_profiler(args)
    # Allow profiler some "dead time" before starting the computation.
    time.sleep(3)
    proc2 = start_script(args, unknown)

    # Keep this process alive until both subprocesses are done,
    # but don't block on either one.
    while proc1.poll() is None or proc2.poll() is None:
        time.sleep(1)


if __name__ == '__main__':
    main()
