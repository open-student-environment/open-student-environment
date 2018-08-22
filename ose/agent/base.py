"""Base class for agents"""

import json


class Role(object):
    TEACHER = 'user:enseignant'
    STUDENT = 'user:eleve'


class Agent(object):

    def __init__(self, name, role=None, groups=[], env=None):
        self.name = name
        self.role = role
        self.groups = groups
        self.env = env

    def __repr__(self):
        return "{} ({})".format(self.name, self.role)

    def update(self, statements):
        pass


def load_agents(filename):
    """
    Loads agent data from JSON file

    Arguments
    ---------
    filename: str
        location of the agent datafile

    Returns
    -------
    agents: list[Agents]
        List of agents
    """

    agents = []
    with open(filename) as f:
        for line in f.readlines():
            js = json.loads(line)
            name = js['uuid']
            role = js['role']
            groups = js['organizations']
            if js['uai'] is not None:
                school = {'id': js['uai'], 'label': js['uai'], 'type': 'school'}
                groups.append(school)
            agent = Agent(name, role, groups)
            agents.append(agent)
    return agents
