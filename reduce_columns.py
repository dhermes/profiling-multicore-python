import colorama
import six


# http://ascii-table.com/ansi-escape-sequences.php
ESCAPE_BEGIN = b'\x1b['
FUNKY_SEQ = b'\x1b[0;0m\x1b[2K\x1b7'
# (value)l
# (value1;...;valueN)m
HEADER_BLOCK = (
    'usr', ' ', 'sys', ' ', 'idl', ' ',
    'wai', ' ', 'hiq', ' ', 'siq',
)
UNUSED_HEADERS = ('idl', 'wai', 'hiq', 'siq')


class AnsiSeq(object):

    def __init__(self, value):
        self.value = value


def add_key(key, value, mapping):
    if key in mapping:
        raise KeyError('Already exists', key)
    mapping[key] = value


def reverse_colorama():
    # b'\x1b' == ESC == chr(27)
    result = {}
    color_obj_names = ('Back', 'Fore', 'Style')
    for name in color_obj_names:
        color_obj = getattr(colorama, name)
        for key, value in six.iteritems(color_obj.__dict__):
            add_key(value, (name, key), result)

    add_key(b'\x1b[7l', (None, 'Disable Wrap'), result)
    add_key(b'\x1b[0;34m', (None, 'Blue, off'), result)
    add_key(b'\x1b[0;0m', (None, None), result)
    add_key(b'\x1b[1;34m', (None, None), result)
    add_key(b'\x1b[4m', (None, None), result)
    add_key(b'\x1b[0;37m', (None, None), result)
    add_key(b'\x1b[1;31m', (None, None), result)
    add_key(b'\x1b[1;32m', (None, None), result)
    add_key(b'\x1b[1;30m', (None, None), result)
    add_key(b'\x1b[1;33m', (None, None), result)
    # add_key(b'\x1b[2K', (None, None), result)

    return result


def startswith_seq(line, reverse_map):
    is_escape = line.startswith(ESCAPE_BEGIN)
    if line.startswith(b'\x1b') and not is_escape:
        raise ValueError('Strange escape', line[:10])

    for seq in six.iterkeys(reverse_map):
        if line.startswith(seq):
            return AnsiSeq(seq)

    if is_escape:
        raise ValueError('Unknown Escape sequence', line[:10])


def tokenize(line, reverse_map):
    result = []
    curr_str = b''
    while line:
        seq = startswith_seq(line, reverse_map)
        if seq is None:
            curr_str += line[0]
            line = line[1:]
        else:
            if curr_str:
                result.append(curr_str)
            result.append(seq)
            curr_str = b''
            line = line[len(seq.value):]

    if curr_str:
        result.append(curr_str)

    return result


def main():
    reverse_map = reverse_colorama()

    with open('dstat-colors.txt', 'rb') as file_obj:
        content = file_obj.read()
    assert content.count(FUNKY_SEQ) == 12
    content = content.replace(FUNKY_SEQ, b'')

    lines = [line.rstrip(b'\r') for line in content.split('\n')]
    T = []
    for line in lines:
        T.append(tokenize(line, reverse_map))

    headers = T[2]
    columns = [v for v in headers if not isinstance(v, AnsiSeq)]
    expected = ('     time     ', '|')
    expected += HEADER_BLOCK + (':',)  # 0
    expected += HEADER_BLOCK + (':',)  # 1
    expected += HEADER_BLOCK + (':',)  # 2
    expected += HEADER_BLOCK + (':',)  # 3
    expected += HEADER_BLOCK + (':',)  # 4
    expected += HEADER_BLOCK + (':',)  # 5
    expected += HEADER_BLOCK + (':',)  # 6
    expected += HEADER_BLOCK           # 7
    expected += ('|', ' used', ' ', ' free')
    assert tuple(columns) == expected
    bad_inds = {}
    for index, value in enumerate(headers):
        if value in UNUSED_HEADERS:
            if value == b'idl':
                add_key(index - 4, True, bad_inds)
                assert headers[index - 4].value == b'\x1b[0;0m'
                add_key(index - 3, True, bad_inds)
                assert headers[index - 3] == b' '
                add_key(index - 2, True, bad_inds)
                assert headers[index - 2].value == b'\x1b[1;34m'

            add_key(index - 1, True, bad_inds)
            assert headers[index - 1].value == b'\x1b[4m'
            add_key(index, True, bad_inds)
            add_key(index + 1, True, bad_inds)
            assert headers[index + 1].value == b'\x1b[0;0m'
            if value == b'siq':
                add_key(index + 2, True, bad_inds)
                assert headers[index + 2].value == b'\x1b[0;34m'
            else:
                add_key(index + 2, True, bad_inds)
                assert headers[index + 2] == b' '
                add_key(index + 3, True, bad_inds)
                assert headers[index + 3].value == b'\x1b[1;34m'


    new_lines = []
    # Start with T[1], ignore T[0]
    section_headers = T[1]
    curr_parts = []
    for val in section_headers:
        if isinstance(val, AnsiSeq):
            curr_parts.append(val.value)
        else:
            if val.startswith(b'-------cpu'):
                assert len(val) == 23
                assert val[11:] == b'-usage------'
                val = b'-' + val[7:11] + b'--'

            curr_parts.append(val)
    new_lines.append(''.join(curr_parts))
    # Then T[2], which is special
    curr_parts = []
    for index, val in enumerate(headers):
        if index in bad_inds:
            continue

        if isinstance(val, AnsiSeq):
            curr_parts.append(val.value)
        else:
            curr_parts.append(val)
    new_lines.append(''.join(curr_parts))
    # Then T[3:], which has actual data
    for data_row in T[3:-1]:
        bad_inds = {}
        strip_inds = {}
        value_ind = 0
        for index, val in enumerate(data_row):
            if not isinstance(val, AnsiSeq):
                if 0 < value_ind < 57:
                    modular_val = value_ind % 7
                    if modular_val in (0, 4, 5, 6):
                        add_key(index - 1, True, bad_inds)
                        assert isinstance(data_row[index - 1], AnsiSeq)
                        add_key(index, True, bad_inds)
                    elif modular_val == 3:
                        add_key(index, True, strip_inds)
                # Update at the end
                value_ind += 1
        assert value_ind == 62
        curr_parts = []
        for index, val in enumerate(data_row):
            if index in bad_inds:
                continue

            if isinstance(val, AnsiSeq):
                curr_parts.append(val.value)
            else:
                if index in strip_inds:
                    val = val.rstrip()
                    strip_inds.pop(index)
                curr_parts.append(val)

        assert strip_inds == {}
        new_lines.append(''.join(curr_parts))


    with open('dstat-colors-reduced.txt', 'wb') as file_obj:
        file_obj.write(b'\n'.join(new_lines))


if __name__ == '__main__':
    main()
