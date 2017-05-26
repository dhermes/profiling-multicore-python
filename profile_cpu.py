import argparse
import collections

import psutil  # 5.2.2
import six  # 1.10.0


DEFAULT_INTERVAL = 1.0


def profile(total_intervals, interval=DEFAULT_INTERVAL):
    # NOTE: Assumes total_intervals is a positive integer.
    all_info = []
    for _ in six.moves.xrange(total_intervals):
        loc_info = psutil.cpu_times_percent(interval=interval, percpu=True)
        all_info.append(loc_info)

    return all_info


def process_info(all_info):
    cpu_time_series = {
        'user': collections.defaultdict(list),
        'system': collections.defaultdict(list),
    }
    for loc_info in all_info:
        for index, cpu_info in enumerate(loc_info):
            cpu_time_series['user'][index].append(cpu_info.user)
            cpu_time_series['system'][index].append(cpu_info.system)

    return cpu_time_series


def plot_info(all_axes, cpu_index, cpu_time_series, num_cpus):
    # NOTE: Importing numpy takes a long time, so it is done here
    #       intentionally (to avoid messing with the
    #       profiling information).
    import numpy as np

    ax = all_axes[cpu_index]
    # Add user info to plot.
    y_vals = cpu_time_series['user'][cpu_index]
    x_vals = np.arange(len(y_vals))
    usr_line, = ax.plot(x_vals, y_vals)
    # Add system info to plot.
    y_vals = cpu_time_series['system'][cpu_index]
    sys_line, = ax.plot(x_vals, y_vals, linestyle='dotted')
    # Set plot attributes.
    ax.set_ylim(-5.0, 105.0)
    ax.set_xticks(x_vals)
    ax.tick_params(labelleft='off')
    if cpu_index != num_cpus - 1:
        ax.tick_params(labelbottom='off')

    return usr_line, sys_line


def plot_all_info(cpu_time_series):
    # NOTE: Importing matplotlib / numpy / seaborn takes a long time, so
    #       it is done here intentionally (to avoid messing with the
    #       profiling information).
    import matplotlib.pyplot as plt
    import seaborn

    num_cpus = len(cpu_time_series['user'])
    rows = num_cpus
    cols = 1
    fig, all_axes = plt.subplots(rows, cols)
    all_axes = all_axes.flatten()

    for cpu_index in six.moves.xrange(num_cpus):
        usr_line, sys_line = plot_info(
            all_axes, cpu_index, cpu_time_series, num_cpus)

    fig.legend((usr_line, sys_line), ('User', 'System'), loc='upper right')
    plt.show()


def main():
    parser = argparse.ArgumentParser(
        description='Profile CPU usage across cores.')
    parser.add_argument(
        '--total-intervals', dest='total_intervals',
        type=int, required=True,
        help='Total number of intervals to profile for.')
    parser.add_argument(
        '--interval', type=float, default=DEFAULT_INTERVAL,
        help='The sample interval during profiling.')

    args = parser.parse_args()
    all_info = profile(args.total_intervals, interval=args.interval)
    cpu_time_series = process_info(all_info)
    plot_all_info(cpu_time_series)


if __name__ == '__main__':
    main()
