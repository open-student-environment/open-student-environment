""" Simulation environment """

import json
from collections import defaultdict


class Environment(object):

    def __init__(self, students=[], statements=[]):
        """
        A Class for modeling the environment.

        Parameters
        ----------

        students: list[Student]
            A list of students

        statements: list[statements]
            A list of statements in xAPI format
        """
        self.students = dict()
        self.statements = defaultdict(list)

        for s in students:
            self.add_student(s)
        for s in statements:
            self.add_statement(s)
        else:
            self.statements = {s.name: [] for s in self.students.values()}

    def add_student(self, student):
        student.env = self
        self.students[student.name] = student
        statements = self.statements[student.name]
        if statements:
            self.students[student.name].update(statements)

    def add_statement(self, statement):
        self.statements[statement['actor']].append(statement)

    def simulate(self, tmax, verbose=False):
        """
        Simulate the interaction of students with resources
        Parameters
        ----------
        tmax: float
            End time for the simulation
        """
        res = []
        tmin = 0
        while tmin < tmax:
            tmin = tmax
            for s in self.students.values():
                statement = s.study()
                t = statement['timestamp']
                tmin = min(t, tmin)
                if t < tmax:
                    res.append(statement)
                    if verbose:
                        print("statement: {}".format(statement))
        return res


def load_json_statements(statements_file):
    """
    Parameters
    ---------
    statements : JSON file contains xAPI statements
    Return
    ---------
    statements : a list of statements extracted from the JSON file.
    """
    statements = json.load(open(statements_file, "r"))

    return statements


def extract_information(statement):
    res = {'actor': eval(statement['actor'])['account']['name'],
           'verb': eval(statement['verb'])['display'],
           'timestamp': statement['timestamp']}
    return res
