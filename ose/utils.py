"""A set of utilities to work with xAPI and other data formats."""

import json
import os


def load_agent_data(filename):

    data = []
    with open(filename) as f:
        for line in f.readlines():
            data.append(json.loads(line))
    return data


if __name__ == "__main__":
    base_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir))
    filename = os.path.join(base_path, 'data/accounts-brneac3-0-20180630.json')
    data = load_agent_data(filename)
    print(data[0])
