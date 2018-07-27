""" Simulation environment """

import json
from collections import defaultdict
import functools
import numpy as np

class Environment(object):


    def __init__(self, students, statements):
        """
        A Class for modeling the environment.

        Parameters
        ----------

        students: list[Student]
            A list of students

        statements: list[statements]
            A list of statements in xAPI format
        """
        self.students = self._create_students_hash(students)
        self.statements = self._create_students_statements(statements)
        self._update_students_statements()

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
            for s in self.students:
                statement = s.study()
                t = statement['timestamp']
                tmin = min(t, tmin)
                if t < tmax:
                    res.append(statement)
                    if verbose:
                        print("statement: {}".format(statement))
        return res

    def _create_students_hash(self,students):
        """
        This method create a student hash that
        :param students:
        :return:
        """
        student_hash = dict()
        for s in students:
            s.env = self
            student_hash[s.name] = s
        return student_hash

    def _update_students_statements(self):
        """
        Update the
        :return:
        """
        for s in self.students.keys():
            s_statements = self.statements[s]
            if s_statements :
                self.students[s].update(s_statements)

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
        statements = json.load(open(statements_file,"r"))

        return statements

    def add_statement(self,statement):
        self.statements[statement["name"]].add(statement)

def _create_students_statements(statements):
    statements_hash = dict()
    for s in statements :
        statements_hash[s["name"]].add(s)
    return statements_hash

def extract_information(statement):
    res = {"name": eval(statement["actor"])["account"]["name"],
           "verb": eval(statement["verb"])["display"],
           "timestamp": statement["timestamp"]}
    return res










