""" Statement handler """

from datetime import datetime
import json


def load_statements(filename):
    """
    Load xAPI statements from a json file.

    Parameters
    ----------
    filename: str
        The path to the filename

    Returns
    -------
    statement: list[statements]
        Returns a OSE compatible list of statements.
    """
    data = []
    with open(filename) as f:
        for line in f.readlines():
            data.append(json.loads(line))

    stats = []
    for s in data:
        stats.append(extract_information(s))

    return stats


def timestring_to_timestamp(timestring, form):
    """
    Convert a string timestamp to a float epoch.

    Parameters
    ----------
    timestamp: str
        The timestamp to transform.

    form: str
        The `format` of the given timestamp to cast into a datetime object.

    Returns
    -------
    epoch: float
        The epoch equivalent representation of the timestamp string.
    """
    epoch = datetime(1970, 1, 1)
    dt = datetime.strptime(timestring.split('.')[0], form)
    td = dt - epoch
    return td.total_seconds()


def extract_information(statement):
    """
    Extract information from a well formated xAPI statement. Infers the
    datetime format to be `'%Y-%m-%dT%H:%M:%S'`.

    Parameters
    ----------
    statement: dict
        An xAPI statement.

    form: str
        The `format` of the given timestamp to cast into a datetime object.

    Returns
    -------
    statement: dict
        Returns a dict, OSE compatible statement.
    """
    form = '%Y-%m-%dT%H:%M:%S'
    res = {'actor': statement['actor']['account']['name'],
           'verb': statement['verb']['id'],
           'timestamp': timestring_to_timestamp(statement['timestamp'], form)}
    return res
