import argparse
import collections
import json
import os
import platform
import shutil
import sys
import tempfile
import uuid

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


def make_rectangular(data_dict):
    # Make sure keys are 0,1,...,N-1  (for N CPUs)
    key_vals = sorted(map(int, six.iterkeys(data_dict)))
    assert key_vals == list(six.moves.xrange(len(key_vals)))
    # Make sure all are lists.
    all_types = set(map(type, six.itervalues(data_dict)))
    assert all_types == set([list])
    # Make sure all have the same number of observations.
    all_lens = set(map(len, six.itervalues(data_dict)))
    assert len(all_lens) == 1
    num_observations = all_lens.pop()

    return [data_dict[cpu_id] for cpu_id in key_vals]


def shape(rectangle):
    assert isinstance(rectangle, list)
    num_rows = len(rectangle)
    assert set(map(type, rectangle)) == set([list])

    all_lens = set(map(len, rectangle))
    assert len(all_lens) == 1
    num_cols = all_lens.pop()

    return num_rows, num_cols


def process_info(all_info, interval, pin_cpu):
    cpu_time_series = {
        'id': str(uuid.uuid4()),
        'interval': interval,
        'platform': platform.platform(),
        'system': collections.defaultdict(list),
        'pin_cpu': pin_cpu,
        'user': collections.defaultdict(list),
        'version': sys.version,
    }
    for loc_info in all_info:
        for index, cpu_info in enumerate(loc_info):
            cpu_time_series['user'][index].append(cpu_info.user)
            cpu_time_series['system'][index].append(cpu_info.system)

    # Ditch defaultdict() and use rectangular list of lists.
    user_data = make_rectangular(cpu_time_series['user'])
    system_data = make_rectangular(cpu_time_series['system'])
    assert shape(user_data) == shape(system_data)
    cpu_time_series['user'] = user_data
    cpu_time_series['system'] = system_data

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


def plot_all_info(cpu_time_series, filename_base):
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

    interval = cpu_time_series['interval']
    for cpu_index in six.moves.xrange(num_cpus):
        usr_line, sys_line = plot_info(
            all_axes, cpu_index, cpu_time_series, num_cpus, interval)

    fig.legend((usr_line, sys_line), ('User', 'System'), loc='upper right')
    fig.set_size_inches(8.0, 8.14)
    fig.tight_layout()
    if filename_base is None:
        plt.show()
        print('Finished {}'.format(cpu_time_series['id']))
    else:
        filename = '{}-{}.png'.format(filename_base, cpu_time_series['id'])
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
        json.dump(
            all_data, file_obj, sort_keys=True,
            indent=2, separators=(',', ': '))
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
        'The base filename to save the plot into (will be augmented with a '
        'unique ID). If not provided, the plot will just be displayed '
        'interactively.')
    parser.add_argument(
        '--filename-base', dest='filename_base', help=filename_help)
    parser.add_argument(
        '--data-id', dest='data_id',
        help='Identifier for the data when being saved.')
    pin_cpu_help = (
        'Indicates if each process/thread should be pinned '
        'to a given CPU.')
    parser.add_argument(
        '--pin-cpu', dest='pin_cpu',
        action='store_true', help=pin_cpu_help)

    return parser.parse_args()


def main():
    args = get_args()
    all_info = profile(args.total_intervals, interval=args.interval)
    cpu_time_series = process_info(all_info, args.interval, args.pin_cpu)
    plot_all_info(cpu_time_series, args.filename_base)
    save_data(cpu_time_series, args.data_id)


if __name__ == '__main__':
    main()
