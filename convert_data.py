import copy
import json
import os
import shutil
import tempfile

import six


CURR_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_FILENAME = os.path.join(CURR_DIR, 'profiles.json')


def transform_dict(value):
    assert isinstance(value, dict)
    existing = set(['user', 'system', 'interval', 'use_setaffinity'])
    assert set(value.keys()) == existing
    new_value = copy.deepcopy(value)
    # sys.version
    new_value['version'] = (
        '2.7.13 (default, Jan  5 2017, 18:58:25) \n[GCC 5.4.0 20160609]')
    # platform.platform()
    new_value['platform'] = (
        'Linux-4.4.0-78-generic-x86_64-with-debian-stretch-sid')
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
