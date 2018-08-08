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


def get_agents_graph(data):
    """
    Extracts adjancy information from the list of agents

    Arguments
    ---------
    data: list[Agents]
        Agents datastructure

    Return
    ------
    adjancy: dict [str -> str]
    """
    agents = defaultdict(dict)
    adjancy = defaultdict(list)
    for user in data:
        username = user['uuid']
        role = user['role']
        agents[username] = role
        if role == 'user:eleve':
            for g in user['organizations']:
                adjancy[g['id']].append(username)
                agents[g['id']] = 'group'
        if role == 'user:enseignant':
            for g in user['organizations']:
                adjancy[username].append(g['id'])
            if user['uai']is not None:
                school = user['uai'].replace(',', '|')
                adjancy[school].append(username)
                agents[school] = 'school'
    return agents, adjancy


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
        f.write('nodedef> name VARCHAR, role VARCHAR\n')
        for name, role in nodes.items():
            f.write("{}, {}\n".format(name, role))
        f.write('edgedef> node1 VARCHAR, node2 VARCHAR, weight DOUBLE\n')
        for parent, children in list(adjancy.items()):
            for child in children:
                f.write("{}, {}, {}\n".format(parent, child, 1))
