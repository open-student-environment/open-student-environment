""" Statement handler """
from datetime import datetime
import json
import os
from pytz import timezone


class Statement(object):

    def __init__(self, actor, verb, timestamp):
        self.actor = actor
        self.verb = verb
        self.timestamp = timestring_to_timestamp(timestamp)


def load_file(filename):
    """
    Load a json filename based in `open-student-environment/filename`

    Parameters
    ----------
    filename: str
        The path to the filename

    Returns
    -------
    statement: list[statements]
        Returns an xAPI list of statements.
    """
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             os.pardir))
    filename = os.path.join(base_path, filename)
    data = []
    with open(filename) as f:
        for line in f.readlines():
            data.append(json.loads(line))
    return data


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
    epoch = datetime(1970,1,1)
    dt = datetime.strptime(timestring.split('.')[0], form)
    td = dt - epoch
    return td.total_seconds()




def extract_information_educlever(statement):
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


def load_statements(statements):
    """
    Takes a list of json formatted xAPI statements and returns a OSE
    compatible statement list.

    Parameters
    ----------
    statement: list[statements]
        A list of xAPI statements.

    Returns
    -------
    statement: list[statements]
        Returns a OSE compatible list of statements.
    """
    stats = []
    for s in statements:
        stats.append(extract_information_educlever(s))
    return stats
