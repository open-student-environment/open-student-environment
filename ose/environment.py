""" Simulation environment """

import json
from collections import defaultdict


class Environment(object):

    def __init__(self, students, statements=None):
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
        self._create_students_hash(students)
        if statements is not None :
            self.statements = _create_students_statements(statements)
            self._update_students_statements()
        else :
            self.statements = {s.name : [] for s in self.students.values()}

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
        while(tmin < tmax):
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

    def _create_students_hash(self, students):
        for s in students:
            self.add_student(s)

    def add_student(self, student):
        student.env = self
        self.students[student.name] = student

    def _update_students_statements(self):
        """
        Update the students statements
        :return:
        """
        for s_name in self.students.keys():
            s_name_statements = self.statements[s_name]
            if s_name_statements:
                self.students[s_name].update(s_name_statements)

    @staticmethod
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

    def add_statement(self, statement):
        self.statements[statement["actor"]].append(statement)


def _create_students_statements(statements):
    """
    This method takes
    :param statements:
    :return:
    """
    statements_hash = defaultdict(list)
    for s in statements:
        statements_hash[s['actor']].append(s)
    return statements_hash


def extract_information(statement):
    res = {"actor": eval(statement["actor"])["account"]["name"],
           "verb": eval(statement["verb"])["display"],
           "timestamp": statement["timestamp"]}
    return res










