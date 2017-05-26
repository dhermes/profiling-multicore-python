import argparse
import collections
import json
import os
import shutil
import tempfile

import psutil  # 5.2.2
import six  # 1.10.0


DEFAULT_INTERVAL = 1.0
CURR_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_FILENAME = os.path.join(CURR_DIR, 'profiles.json')


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


def plot_info(all_axes, cpu_index, cpu_time_series, num_cpus, interval):
    # NOTE: Importing numpy takes a long time, so it is done here
    #       intentionally (to avoid messing with the
    #       profiling information).
    import numpy as np  # 1.12.1

    ax = all_axes[cpu_index]
    # Add user info to plot.
    y_vals = cpu_time_series['user'][cpu_index]
    x_vals = np.arange(len(y_vals)) * interval
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


def plot_all_info(cpu_time_series, interval, filename):
    # NOTE: Importing matplotlib / numpy / seaborn takes a long time, so
    #       it is done here intentionally (to avoid messing with the
    #       profiling information).
    import matplotlib.pyplot as plt  # 2.0.2
    import seaborn  # 0.7.1

    num_cpus = len(cpu_time_series['user'])
    rows = num_cpus
    cols = 1
    fig, all_axes = plt.subplots(rows, cols)
    all_axes = all_axes.flatten()

    for cpu_index in six.moves.xrange(num_cpus):
        usr_line, sys_line = plot_info(
            all_axes, cpu_index, cpu_time_series, num_cpus, interval)

    fig.legend((usr_line, sys_line), ('User', 'System'), loc='upper right')
    fig.set_size_inches(8.0, 8.14)
    fig.tight_layout()
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
        print('Saved {}'.format(filename))


def save_data(cpu_time_series, data_id):
    if data_id is None:
        print('No data ID provided, data is not being saved.')
        return

    with open(DATA_FILENAME, 'r') as file_obj:
        all_data = json.load(file_obj)

    data_group = all_data.setdefault(data_id, [])
    data_group.append(cpu_time_series)

    _, filename = tempfile.mkstemp()
    with open(filename, 'w') as file_obj:
        json.dump(all_data, file_obj, indent=2, separators=(',', ': '))
        file_obj.write('\n')

    shutil.move(filename, DATA_FILENAME)


def get_args():
    parser = argparse.ArgumentParser(
        description='Profile CPU usage across cores.')
    parser.add_argument(
        '--total-intervals', dest='total_intervals',
        type=int, required=True,
        help='Total number of intervals to profile for.')
    parser.add_argument(
        '--interval', type=float, default=DEFAULT_INTERVAL,
        help='The sample interval during profiling.')
    filename_help = (
        'The filename to save the plot into. If not provided, the plot '
        'will just be displayed interactively.')
    parser.add_argument('--filename', help=filename_help)
    parser.add_argument(
        '--data-id', dest='data_id',
        help='Identifier for the data when being saved.')

    return parser.parse_args()


def main():
    args = get_args()
    all_info = profile(args.total_intervals, interval=args.interval)
    cpu_time_series = process_info(all_info)
    plot_all_info(cpu_time_series, args.interval, args.filename)
    save_data(cpu_time_series, args.data_id)


if __name__ == '__main__':
    main()
