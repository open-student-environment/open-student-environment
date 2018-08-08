"""A set of utilities to work with xAPI and other data formats."""

import json
import os

from collections import defaultdict


def load_agent_data(filename):
    """
    Loads agent data from JSON file

    Arguments
    ---------
    filename: str
        location of the agent datafile

    Returns
    -------
    data: list[Agents]
        List of agents
    """

    data = []
    with open(filename) as f:
        for line in f.readlines():
            data.append(json.loads(line))
    return data


def build_graph_from_data(data):
    """
    Returns the adjancy graph of the actors (students, teachers, school)

    Arguments
    ---------
    filename: str
        Agents datastructure

    Return
    ______
    nodes: list[str]
        List of agent's names

    adjancy: dict(str: [Agents])
        Adjancy lists indexed by agent name (agent_names -> agents)
    """
    groups = defaultdict(list)
    for user in data:
        username = user['uuid']
        role = user['role']
        if role == 'user:enseignant':
            for g in user['organizations']:
                groups[g['id']].append(username)
    adjancy = defaultdict(set)

    for user in data:
        username = user['uuid']
        role = user['role']
        for g in user['organizations']:
            for parent in groups[g['id']]:
                adjancy[parent].add(username)
        if role == 'user:enseignant':
            if user['uai'] is not None:
                adjancy[user['uai'].replace('.', ' ')].add(username)

    nodes = set(user['uuid'] for user in data)

    return nodes, adjancy


def graph2gephi(nodes, adjancy, filename='test.gdf'):
    """
    Formats the adjancy list to `.gdf` (Gephi file)

    Arguments
    ---------
    nodes: list[str]
        List of agent's names

    adjancy: dict(str: [Agents])
        Adjancy lists indexed by agent name (agent_names -> agents)
    """
    with open(filename, 'w') as f:
        f.write('nodedef> name VARCHAR\n')
        for node in nodes:
            f.write("{}\n".format(node))
        f.write('edgedef> node1 VARCHAR, node2 VARCHAR, weight DOUBLE\n')
        for parent, children in list(adjancy.items()):
            for child in children:
                f.write("{}, {}, {}\n".format(parent, child, 1))

def filter_by_users(nodes, adjancy, user_reference):
    """
    Takes a list of nodes and an adjancy list. Remove the non referenced
    users from the passed user reference list.

    Arguments
    ---------
    nodes: set[str]
        List of agent's names.

    adjancy: dict(str: [Agents])
        Adjancy lists indexed by agent name (agent_names -> agents).

    user_reference: set[str]
        The reference set of users.

    Returns
    -------
    nodes_clean:
        The filtered nodes set.

    nodes_clean:
        The filtered adjancy list.
    """
    nodes_clean = nodes.intersection(user_reference)
    adjancy_clean = {}
    for k,v in adjancy.items():
        if k in user_reference:
            adjancy_clean[k] = v.intersection(user_reference)
    return nodes_clean, adjancy_clean



if __name__ == "__main__":
    base_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir))
    filename = os.path.join(base_path, 'data/accounts-brneac3-0-20180630.json')
    data = load_agent_data(filename)
    print(data[0])
