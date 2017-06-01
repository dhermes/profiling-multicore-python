import json
import os
import shutil
import tempfile

import six


CURR_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_FILENAME = os.path.join(CURR_DIR, 'profiles.json')


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

    return [data_dict[str(cpu_id)] for cpu_id in key_vals]


def transform_dict(value):
    assert isinstance(value, dict)
    assert set(value.keys()) == set(['user', 'system'])
    new_value = {
        'user': make_rectangular(value['user']),
        'system': make_rectangular(value['system']),
        'interval': 1.0,
    }
    return new_value


def transform_list(value):
    assert isinstance(value, list)
    return [transform_dict(element) for element in value]


def main():
    with open(DATA_FILENAME, 'rb') as file_obj:
        all_data = json.load(file_obj)

    new_data = {}
    for key, value in six.iteritems(all_data):
        new_data[key] = transform_list(value)

    _, filename = tempfile.mkstemp()
    with open(filename, 'w') as file_obj:
        json.dump(
            new_data, file_obj, sort_keys=True,
            indent=2, separators=(',', ': '))
        file_obj.write('\n')

    shutil.move(filename, DATA_FILENAME)


if __name__ == '__main__':
    main()
