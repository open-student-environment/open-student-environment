from datetime import datetime
import json
import os

DATA_FILE = "unique_example_maskott.json"


def load_json_statements(statements_file):
    statements = json.load(open(statements_file, "r"))
    return statements


def load_file(filename):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), \
                                             os.pardir))
    filename = os.path.join(base_path, 'data/{}'.format(filename))
    data = []
    with open(filename) as f:
        for line in f.readlines():
            data.append(json.loads(line))
    return data


def _convert_datetime_to_epoch(d_time):
    return float(d_time.strftime('%s'))


def _timestamp_to_float(timestamp, form):
    timestamp = timestamp.split('.')[0]
    d_time = datetime.strptime(timestamp, form)
    return _convert_datetime_to_epoch(d_time)


def extract_information_educlever(statement):
    form = '%Y-%m-%dT%H:%M:%S'
    return {'actor': statement['actor']['account']['name'],
            'verb': statement['verb']['id'],
            'timestamp': _timestamp_to_float(statement['timestamp'], form)}


def extract_information_maskott(statement):
    form = '%Y-%m-%dT%H:%M:%S'
    res = {'actor': eval(statement['actor'])['account']['name'],
           'verb': eval(statement['verb'])['display'],
           'timestamp': statement['timestamp']}
    return res


def load_statements(statements, back_end='educlever'):
    stats = []
    if back_end == 'educlever':
        for s in statements:
            stats.append(extract_information_educlever(s))
    elif back_end == 'maskott':
        for s in statements:
            stats.append(extract_information_educlever(s))
    return stats


def main():
    data = load_file(DATA_FILE)
    statements = load_statements(data)


if __name__ == '__main__':
    main()
